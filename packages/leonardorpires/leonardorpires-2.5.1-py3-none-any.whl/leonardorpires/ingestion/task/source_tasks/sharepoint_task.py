from typing import Optional

from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType

from pyiris.infrastructure import Spark
from pyiris.infrastructure.common.exception import (
    SharePointTaskCouldNotReadFileException,
)
from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.sharepoint.sharepoint_connection import SharePointConnection
from pyiris.infrastructure.spark.spark_mapper import SparkMapper
from pyiris.ingestion.config.file_system_config import FileSystemConfig
from pyiris.ingestion.extract import FileReader
from pyiris.ingestion.extract.readers.sharepoint_reader import SharePointReader
from pyiris.ingestion.load import FileWriter
from pyiris.ingestion.task.entity.sharepoint_task_entity import SharepointTaskEntity
from pyiris.ingestion.task.source_tasks.source_task import SourceTask
from pyiris.ingestion.transform import TransformService
from pyiris.ingestion.utils.utils import TemporaryPath

logger = Logger(__name__)


class SharePointTask(SourceTask):
    """
    This class intends to read a file from a Sharepoint source.

    :param metadata_entity: the dataset metadata object
    :type metadata_entity: pyiris.ingestion.task.entiry.metadata_entity.MetadataEntity

    :param task_entity: the task definition entity object
    :type task_entity: optional, pyiris.ingestion.task.entity.task_entity.TaskEntity

    :param spark_mapper: The Spark mapper object.
    :type spark_mapper: Optional, pyiris.infrastructure.spark.spark_mapper.SparkMapper

    :param engine: The processing engine to be used. Defaults to the Spark object.
    :type engine: Optional, pyiris.infrastructure.spark.spark.Spark

    :param sharepoint_reader: the rabbitmq reader object
    :type sharepoint_reader: Optional, pyiris.ingestion.extract.readers.sharepoint_reader.SharePointReader
    """

    def __init__(
        self,
        task_entity: SharepointTaskEntity,
        metadata_entity: MetadataEntity,
        file_system_config: FileSystemConfig,
        file_writer_engine: FileWriter,
        file_reader: FileReader,
        transform_service: TransformService,
        spark_mapper: Optional[SparkMapper] = None,
        engine: Optional[Spark] = None,
        sharepoint_reader: Optional[SharePointReader] = None,
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

        self.schema = self.spark_mapper.get_schema_definition(
            metadata=metadata_entity.__dict__
        )
        self.file_name = task_entity.name
        self.file_format = task_entity.file_format
        self.temporary_path = TemporaryPath.build()
        self.sharepoint_reader = sharepoint_reader or SharePointReader(
            file_name=self.file_name,
            file_folder=task_entity.file_folder,
            file_format=self.file_format,
            engine=SharePointConnection.build(
                url=task_entity.url,
                client_id=task_entity.client_id,
                client_secret=task_entity.client_secret,
            ),
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temporary_path.cleanup()

    def source_reader(self) -> DataFrame:
        """
        This method is responsible for consume a file from a SharePoint Site, save the file into a temporary directory
        and then read the file with Spark in an appropriate format

        :return: the extracted dataframe
        :rtype: pyspark.sql.dataframe.DataFrame
        """

        spark_schema = StructType.fromJson(self.schema)
        self.sharepoint_reader.consume(temporary_path=self.temporary_path.name)
        try:
            if self.file_format in ("xlsx", "xls"):
                logger.info(f"Reading {self.file_name}.{self.file_format} file")
                dataframe = self.engine.read(
                    format="com.crealytics.spark.excel",
                    path=f"{self.temporary_path.name_without_prefix}/{self.file_name}.{self.file_format}",
                    options={"header": "true", "schema": spark_schema},
                )

            else:
                logger.info("Reading csv file")
                dataframe = self.engine.read(
                    format=self.file_format,
                    path=f"{self.temporary_path.name_without_prefix}",
                    options={"header": "true", "schema": spark_schema},
                )
        except Exception as e:
            raise SharePointTaskCouldNotReadFileException(message=e)

        return dataframe

    @staticmethod
    def build(
        task_entity: SharepointTaskEntity,
        metadata_entity: MetadataEntity,
        engine: Optional[SparkSession] = None,
    ):
        return SharePointTask(
            task_entity=task_entity,
            metadata_entity=metadata_entity,
            engine=engine,
            file_system_config=SharePointTask.build_file_system_config(task_entity),
            file_writer_engine=SharePointTask.build_file_writer_engine(
                SharePointTask.build_file_system_config(task_entity)
            ),
            file_reader=SharePointTask.build_file_reader(task_entity),
            transform_service=SharePointTask.build_transform_service(task_entity),
        )
