from typing import Optional

from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType

from pyiris.infrastructure import Spark
from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.smb.smb_connection import SMBConnection
from pyiris.infrastructure.spark.spark_mapper import SparkMapper
from pyiris.ingestion.config.file_system_config import FileSystemConfig
from pyiris.ingestion.extract import FileReader
from pyiris.ingestion.extract.readers.file_system_reader import FileSystemReader
from pyiris.ingestion.load import FileWriter
from pyiris.ingestion.task.entity.file_system_task_entity import FileSystemTaskEntity
from pyiris.ingestion.task.source_tasks.source_task import SourceTask
from pyiris.ingestion.transform import TransformService

logger = Logger(__name__)


class FileSystemTask(SourceTask):
    """
    This class will run a complete ETL job, from a FileSystem to the Datalake's Trustedzone.

    :param metadata_entity: The dataset metadata object
    :type metadata_entity: pyiris.ingestion.task.entiry.metadata_entity.MetadataEntity

    :param task_entity: The task definition entity object
    :type task_entity: optional, pyiris.ingestion.task.entity.task_entity.TaskEntity

    :param spark_mapper: The Spark mapper object.
    :type spark_mapper: Optional, pyiris.infrastructure.spark.spark_mapper.SparkMapper

    :param engine: The processing engine to be used. Defaults to the Spark object.
    :type engine: Optional, pyiris.infrastructure.spark.spark.Spark

    :param file_system_reader: The File System Reader object.
    :type file_system_reader: Optional, pyiris.ingestion.extract.readers.file_system_reader.FileSystemReader

    """

    def __init__(
        self,
        task_entity: FileSystemTaskEntity,
        metadata_entity: MetadataEntity,
        file_system_config: FileSystemConfig,
        file_writer_engine: FileWriter,
        file_reader: FileReader,
        transform_service: TransformService,
        spark_mapper: Optional[SparkMapper] = None,
        engine: Optional[Spark] = None,
        file_system_reader: Optional[FileSystemReader] = None,
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

        self.column_separator = task_entity.column_separator
        self.has_header = task_entity.has_header
        self.schema = self.spark_mapper.get_schema_definition(
            metadata=metadata_entity.__dict__
        )
        self.file_system_reader = file_system_reader or FileSystemReader(
            file_name=task_entity.name,
            file_path=task_entity.file_path,
            connection_engine=SMBConnection(
                host=task_entity.host,
                username=task_entity.username,
                password=task_entity.password,
            ),
            file_type=task_entity.file_type,
            encoding=task_entity.encoding,
            mode=task_entity.mode,
            newline=task_entity.newline,
        )

    @logger.log_decorator
    def source_reader(self) -> DataFrame:
        """
        This method will read the data and return it as a Spark DataFrame.
        """

        schema = StructType.fromJson(self.schema)
        result = self.file_system_reader.consume(spark=self.engine)
        spark_rdd = self.engine.session.sparkContext.parallelize(result)
        dataframe = (
            self.engine.session.read.option("header", self.has_header)
            .option("schema", schema)
            .option("sep", self.column_separator)
            .csv(spark_rdd)
        )

        logger.info("Reading data from File System")
        return dataframe

    @staticmethod
    def build(
        task_entity: FileSystemTaskEntity,
        metadata_entity: MetadataEntity,
        engine: Optional[SparkSession] = None,
    ):
        return FileSystemTask(
            task_entity=task_entity,
            metadata_entity=metadata_entity,
            engine=engine,
            file_system_config=FileSystemTask.build_file_system_config(task_entity),
            file_writer_engine=FileSystemTask.build_file_writer_engine(
                FileSystemTask.build_file_system_config(task_entity)
            ),
            file_reader=FileSystemTask.build_file_reader(task_entity),
            transform_service=FileSystemTask.build_transform_service(task_entity),
        )
