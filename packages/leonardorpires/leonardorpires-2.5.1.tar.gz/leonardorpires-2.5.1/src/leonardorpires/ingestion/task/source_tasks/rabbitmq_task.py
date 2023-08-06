import json
from typing import Optional, Union

from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession

from pyiris.infrastructure import Spark
from pyiris.infrastructure.common.exception import (
    RabbitMQTaskExecutionTimeoutException,
    RabbitMQTaskInactivityTimeout,
    RabbitMQTaskNoMessagesFoundException,
)
from pyiris.infrastructure.rabbitmq.rabbitmq_connection import RabbitMQConnection
from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.spark.spark_mapper import SparkMapper
from pyiris.infrastructure.thread_local import ThreadLocal
from pyiris.ingestion.config.file_system_config import FileSystemConfig
from pyiris.ingestion.enums.enums import IrisMountNames
from pyiris.ingestion.extract import FileReader
from pyiris.ingestion.load import FileWriter
from pyiris.ingestion.task.entity.rabbitmq_task_entity import RabbitMQTaskEntity
from pyiris.ingestion.task.source_tasks.source_task import SourceTask
from pyiris.ingestion.transform import TransformService

logger = Logger(__name__)


class RabbitMQTask(SourceTask):
    """
    This class intends to read messages in the RabbitMQ queue.
    To read the messages the users need to pass some parameters.

    :param task_entity: the task definition entity object
    :type task_entity: optional, pyiris.ingestion.task.entity.task_entity.TaskEntity

    :param metadata_entity: the dataset metadata object
    :type metadata_entity: pyiris.ingestion.task.entiry.metadata_entity.MetadataEntity

    :param spark_mapper: The Spark mapper object.
    :type spark_mapper: Optional, pyiris.infrastructure.spark.spark_mapper.SparkMapper

    :param engine: The processing engine to be used. Defaults to the Spark object.
    :type engine: Optional, pyiris.infrastructure.spark.spark.Spark

    :param rabbitmq_connection: The RabbitMQ connection object.
    :type rabbitmq_connection: Optional, pyiris.infrastructure.rabbitmq.rabbitmq_connection.RabbitMQConnection
    """

    def __init__(
        self,
        task_entity: RabbitMQTaskEntity,
        metadata_entity: MetadataEntity,
        file_system_config: FileSystemConfig,
        file_writer_engine: FileWriter,
        file_reader: FileReader,
        transform_service: TransformService,
        engine: Optional[Spark] = None,
        spark_mapper: Optional[SparkMapper] = None,
        rabbitmq_connection: Optional[RabbitMQConnection] = None,
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
        self.delivery_tags = list()
        self.queue_name = task_entity.name
        self.execution_timeout = task_entity.execution_timeout
        self.prefetch_count = task_entity.prefetch_count
        self.rabbitmq_connection = rabbitmq_connection or RabbitMQConnection.build(
            host=task_entity.host,
            username=task_entity.login,
            password=task_entity.password,
            vhost=task_entity.vhost,
        )

    @logger.log_decorator
    def definitions(self) -> None:
        dataframe = None
        ThreadLocal.set_rabbitmq_task_start_time()
        self.rabbitmq_connection.call_later(
            delay=self.execution_timeout, callback=self._inactivity_timeout_callback
        )
        channel = self.rabbitmq_connection.channel()

        try:
            if self._queue_has_message(channel=channel):
                channel.basic_qos(prefetch_count=self.prefetch_count)
                channel.basic_consume(
                    queue=self.queue_name, on_message_callback=self.source_reader
                )
                channel.start_consuming()

        except (RabbitMQTaskExecutionTimeoutException, RabbitMQTaskInactivityTimeout):
            source_dataframe = self.parse_dataframe(data=self.messages)
            raw_dataframe = self._raw_definitions(dataframe=source_dataframe)

            channel.basic_ack(delivery_tag=0, multiple=1)
            logger.info(f"Acknowledge {len(self.delivery_tags)} messages")

            dataframe = self._trusted_definitions(dataframe=raw_dataframe)

        except RabbitMQTaskNoMessagesFoundException:
            pass
        except Exception as exception:
            raise exception
        finally:
            self.messages.clear()
            self.delivery_tags.clear()

        return dataframe

    def source_reader(
        self, channel=None, method_frame=None, header_frame=None, body=None
    ):
        self.messages.append(json.loads(body))
        self.delivery_tags.append(method_frame.delivery_tag)
        start_time = ThreadLocal.get_rabbitmq_task_start_time()
        if start_time and start_time >= self.execution_timeout:
            logger.info(f"Total processed messages in memory: {len(self.messages)}")
            raise RabbitMQTaskExecutionTimeoutException()

    def _trusted_definitions(self, dataframe: DataFrame):
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

    def _queue_has_message(
        self, channel
    ) -> Union[bool, RabbitMQTaskNoMessagesFoundException]:
        queue = channel.queue_declare(self.queue_name, durable=True)
        total_messages = queue.method.message_count
        if total_messages > 0:
            return True
        else:
            raise RabbitMQTaskNoMessagesFoundException()

    def _inactivity_timeout_callback(self):
        raise RabbitMQTaskInactivityTimeout()

    @staticmethod
    def build(
        task_entity: RabbitMQTaskEntity,
        metadata_entity: MetadataEntity,
        engine: Optional[SparkSession] = None,
    ):
        return RabbitMQTask(
            task_entity=task_entity,
            metadata_entity=metadata_entity,
            engine=engine,
            file_system_config=RabbitMQTask.build_file_system_config(task_entity),
            file_writer_engine=RabbitMQTask.build_file_writer_engine(
                RabbitMQTask.build_file_system_config(task_entity)
            ),
            file_reader=RabbitMQTask.build_file_reader(task_entity),
            transform_service=RabbitMQTask.build_transform_service(task_entity),
        )
