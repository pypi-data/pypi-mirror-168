from abc import abstractmethod
from typing import Optional
from uuid import uuid4

from pyspark.sql import DataFrame

from pyiris.infrastructure import Spark
from pyiris.infrastructure.common.exception import PyIrisTaskException
from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.spark.spark_mapper import SparkMapper
from pyiris.infrastructure.thread_local import ThreadLocal
from pyiris.ingestion.config.file_system_config import FileSystemConfig
from pyiris.ingestion.enums.enums import IrisMountNames
from pyiris.ingestion.extract import FileReader
from pyiris.ingestion.load import FileWriter
from pyiris.ingestion.task.task_decorator import TaskDecorator
from pyiris.ingestion.transform.transform_service import TransformService

logger = Logger(__name__)


class BaseTask(object):
    """
    This class intends to be the base task class. All the params or methods that intends to be implemented in all the
    tasks classes, has to be defined here.

    :param metadata_entity: the dataset metadata object
    :type metadata_entity: pyiris.ingestion.task.entiry.metadata_entity.MetadataEntity

    :param task_entity: the task definition entity object
    :type task_entity: Union[pyiris.ingestion.task.entity.task_entity.TaskEntity,
                           pyiris.ingestion.task.entity.rabbit_mq_task_entity.RabbitMQTaskEntity,
                           pyiris.ingestion.task.entity.jdbc_task_entity.JdbcTaskEntity,
                           pyiris.ingestion.task.entity.file_system_task_entity.FileSystemTaskEntity,
                           pyiris.ingestion.task.entity.restapi_task_entity.RestApiTaskEntity,
                           pyiris.ingestion.task.entity.sharepoint_task_entity.SharepointTaskEntity]

    :param file_system_config: The File System config object.
    :type file_system_config: pyiris.ingestion.config.file_system_config.FileSystemConfig

    :param file_writer_engine: The file writer object.
    :type file_writer_engine: pyiris.ingestion.load.FileWriter

    :param file_reader: The file reader object.
    :type file_reader: pyiris.ingestion.extract.FileReader

    :param transform_service: The transformations service object.
    :type transform_service: pyiris.ingestion.transform.transform_service.TransformService

    :param spark_mapper: The Spark mapper object.
    :type spark_mapper: Optional, pyiris.infrastructure.spark.spark_mapper.SparkMapper

    :param engine: The processing engine to be used. Defaults to the Spark object.
    :type engine: Optional, pyiris.infrastructure.spark.spark.Spark
    """

    def __init__(
        self,
        task_entity,
        metadata_entity: MetadataEntity,
        file_system_config: FileSystemConfig,
        file_writer_engine: FileWriter,
        file_reader: FileReader,
        transform_service: TransformService,
        engine: Optional[Spark] = None,
        spark_mapper: Optional[SparkMapper] = None,
    ):
        self.task_entity = task_entity
        self.metadata_entity = metadata_entity
        self.file_system_config = file_system_config
        self.file_writer_engine = file_writer_engine
        self.file_reader = file_reader
        self.transform_service = transform_service
        self.engine = engine or Spark()
        self.spark_mapper = spark_mapper or SparkMapper()

    @abstractmethod
    def definitions(self) -> DataFrame:
        pass

    @logger.log_decorator
    @TaskDecorator()
    def run(self):
        ThreadLocal.set_request_id(str(uuid4()))
        try:
            return self.definitions()
        except Exception as e:
            logger.error(message="Error when try to process Task.")
            raise PyIrisTaskException(message=e)

    @staticmethod
    def build_file_system_config(task_entity):
        return FileSystemConfig(
            format=task_entity.format,
            path=task_entity.path,
            country=task_entity.country,
            mount_name=IrisMountNames.RAWZONE.value,
            mode=task_entity.sync_mode,
            partition_by=task_entity.partition_by,
            base_path=task_entity.base_path,
            options=task_entity.options,
        )

    @staticmethod
    def build_file_writer_engine(file_system_config):
        return FileWriter(config=file_system_config)

    @staticmethod
    def build_file_reader(task_entity):
        return FileReader(
            table_id=task_entity.name,
            country=task_entity.country,
            path=task_entity.path,
            format=task_entity.format,
            base_path=task_entity.base_path,
        )

    @staticmethod
    def build_transform_service(task_entity):
        return TransformService(transformations=task_entity.transformations)
