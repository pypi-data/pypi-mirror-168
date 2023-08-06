import json
from typing import Optional

from azure.servicebus import AutoLockRenewer
from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession

from pyiris.infrastructure import Spark
from pyiris.infrastructure.integration.servicebus.servicebus_connection import (
    ServiceBusConnection,
)
from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.spark.spark_mapper import SparkMapper
from pyiris.ingestion.config.file_system_config import FileSystemConfig
from pyiris.ingestion.enums.enums import IrisMountNames
from pyiris.ingestion.extract import FileReader
from pyiris.ingestion.load import FileWriter
from pyiris.ingestion.task.entity.servicebus_task_entity import ServiceBusTaskEntity
from pyiris.ingestion.task.source_tasks.source_task import SourceTask
from pyiris.ingestion.transform import TransformService

logger = Logger(__name__)


class ServiceBusTask(SourceTask):
    def __init__(
        self,
        task_entity: ServiceBusTaskEntity,
        metadata_entity: MetadataEntity,
        file_system_config: FileSystemConfig,
        file_writer_engine: FileWriter,
        file_reader: FileReader,
        transform_service: TransformService,
        engine: Optional[Spark] = None,
        spark_mapper: Optional[SparkMapper] = None,
        servicebus_connection: Optional[ServiceBusConnection] = None,
    ):
        super().__init__(
            task_entity=task_entity,
            metadata_entity=metadata_entity,
            file_system_config=file_system_config,
            file_writer_engine=file_writer_engine,
            file_reader=file_reader,
            transform_service=transform_service,
            engine=engine,
            spark_mapper=spark_mapper,
        )

        self.messages = list()
        self.task_entity = task_entity
        self.servicebus_connection = (
            servicebus_connection
            or ServiceBusConnection.build(
                connection_string=task_entity.connection_string
            )
        )

    def definitions(self) -> DataFrame:
        try:
            with self.servicebus_connection:
                with AutoLockRenewer() as renewer:
                    with self.servicebus_connection.get_queue_receiver(
                        queue_name=self.task_entity.name,
                        prefetch_count=self.task_entity.max_message_count,
                    ) as receiver:

                        received_messages = receiver.receive_messages(
                            max_message_count=self.task_entity.max_message_count,
                            max_wait_time=self.task_entity.max_wait_time,
                        )

                        for message in received_messages:
                            renewer.register(
                                receiver,
                                message,
                                max_lock_renewal_duration=self.task_entity.max_lock_renewal_duration,
                            )

                            self.messages.append(json.loads(str(message)))

                        logger.info(f"Received {len(self.messages)} messages.")
                        source_dataframe = self.parse_dataframe(data=self.messages)

                        if not source_dataframe.rdd.isEmpty():
                            raw_dataframe = self._raw_definitions(
                                dataframe=source_dataframe
                            )

                            for messages in received_messages:
                                receiver.complete_message(messages)

                            dataframe = self._trusted_definitions(
                                dataframe=raw_dataframe
                            )

        except Exception as exception:
            raise exception
        finally:
            self.messages.clear()

        return dataframe

    def _trusted_definitions(self, dataframe: DataFrame) -> DataFrame:
        zone = IrisMountNames.TRUSTEDZONE.value
        trusted_transformations = self.source_transform_builder.build(
            context=self.task_entity.__dict__, zone=zone
        )
        self.transform_service.transformations = trusted_transformations.transformations
        trusted_dataframe = self.transform_service.handler(dataframe=dataframe)

        self.file_system_config.mount_name = zone
        self.file_writer_engine.config = self.file_system_config
        self.file_writer_engine.write(dataframe=trusted_dataframe)
        return dataframe

    @staticmethod
    def build(
        task_entity: ServiceBusTaskEntity,
        metadata_entity: MetadataEntity,
        engine: Optional[SparkSession] = None,
    ):
        return ServiceBusTask(
            task_entity=task_entity,
            metadata_entity=metadata_entity,
            engine=engine,
            file_system_config=ServiceBusTask.build_file_system_config(task_entity),
            file_writer_engine=ServiceBusTask.build_file_writer_engine(
                ServiceBusTask.build_file_system_config(task_entity)
            ),
            file_reader=ServiceBusTask.build_file_reader(task_entity),
            transform_service=ServiceBusTask.build_transform_service(task_entity),
        )
