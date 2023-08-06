from typing import Optional

from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession

from pyiris.infrastructure.restapi.authenticate import RestApiAuthenticate
from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.spark.spark import Spark
from pyiris.infrastructure.spark.spark_mapper import SparkMapper
from pyiris.ingestion.config.file_system_config import FileSystemConfig
from pyiris.ingestion.extract import FileReader
from pyiris.ingestion.extract.readers.restapi_reader import RestApiReader
from pyiris.ingestion.load import FileWriter
from pyiris.ingestion.task.entity.restapi_task_entity import RestApiTaskEntity
from pyiris.ingestion.task.source_tasks.source_task import SourceTask
from pyiris.ingestion.transform import TransformService

logger = Logger(__name__)


class RestApiTask(SourceTask):
    """
    This class intends to define an etl from a given Rest API to trustedzone.

    :param metadata_entity: the dataset metadata object
    :type metadata_entity: pyiris.ingestion.task.entity.metadata_entity.MetadataEntity

    :param task_entity: the task definition entity object
    :type task_entity: optional, pyiris.ingestion.task.entity.restapi_task_entity.RestApiTaskEntity

    :param spark_mapper: The Spark mapper object.
    :type spark_mapper: Optional, pyiris.infrastructure.spark.spark_mapper.SparkMapper

    :param engine: The processing engine to be used. Defaults to the Spark object.
    :type engine: Optional, pyiris.infrastructure.spark.spark.Spark
    """

    def __init__(
        self,
        task_entity: RestApiTaskEntity,
        metadata_entity: MetadataEntity,
        file_system_config: FileSystemConfig,
        file_writer_engine: FileWriter,
        file_reader: FileReader,
        transform_service: TransformService,
        spark_mapper: Optional[SparkMapper] = None,
        engine: Optional[Spark] = None,
    ):
        super().__init__(
            task_entity=task_entity,
            metadata_entity=metadata_entity,
            file_system_config=file_system_config,
            file_writer_engine=file_writer_engine,
            file_reader=file_reader,
            transform_service=transform_service,
            spark_mapper=spark_mapper,
            engine=engine,
        )
        self.api_id = task_entity.name
        self.url = task_entity.url
        self.method = task_entity.method
        self.response_schema = self.spark_mapper.get_schema_definition(
            metadata=metadata_entity.__dict__
        )
        self.data_response_mapping = task_entity.data_response_mapping
        self.pagination_options = task_entity.options.get("pagination_options") or {}
        self.body = task_entity.options.get("body")
        self.headers = task_entity.options.get("headers")
        self.rest_authenticate = RestApiAuthenticate(
            auth_credentials=task_entity.options.get("auth_credentials")
        )

        self.restapi_reader_engine = RestApiReader(
            api_id=self.api_id,
            url=self.url,
            method=self.method,
            rest_authenticate=self.rest_authenticate,
            response_schema=self.response_schema,
            data_response_mapping=self.data_response_mapping,
            pagination_options=self.pagination_options,
            body=self.body,
            headers=self.headers,
            engine=self.engine,
        )

    @logger.log_decorator
    def source_reader(self) -> DataFrame:
        """
        This consumes method is responsible for consuming the REST API response to Dataframe.

        :return: the result dataframe
        :rtype: pyspark.sql.DataFrame
        """
        return self.restapi_reader_engine.consume()

    @staticmethod
    def build(
        task_entity: RestApiTaskEntity,
        metadata_entity: MetadataEntity,
        engine: Optional[SparkSession] = None,
    ):
        return RestApiTask(
            task_entity=task_entity,
            metadata_entity=metadata_entity,
            engine=engine,
            file_system_config=RestApiTask.build_file_system_config(task_entity),
            file_writer_engine=RestApiTask.build_file_writer_engine(
                RestApiTask.build_file_system_config(task_entity)
            ),
            file_reader=RestApiTask.build_file_reader(task_entity),
            transform_service=RestApiTask.build_transform_service(task_entity),
        )
