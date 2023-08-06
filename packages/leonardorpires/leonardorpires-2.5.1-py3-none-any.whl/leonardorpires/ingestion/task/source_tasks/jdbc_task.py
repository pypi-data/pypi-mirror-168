from typing import Optional

from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession

from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.infrastructure.spark.spark import Spark
from pyiris.infrastructure.spark.spark_mapper import SparkMapper
from pyiris.ingestion.config.file_system_config import FileSystemConfig
from pyiris.ingestion.extract import FileReader
from pyiris.ingestion.extract.readers.jdbc_reader import JdbcReader
from pyiris.ingestion.load import FileWriter
from pyiris.ingestion.task.entity.jdbc_task_entity import JdbcTaskEntity
from pyiris.ingestion.task.source_tasks.source_task import SourceTask
from pyiris.ingestion.transform import TransformService


class JdbcTask(SourceTask):
    """
    This class intends to define an etl from jdbc database to trustedzone.

    :param metadata_entity: the dataset metadata object
    :type metadata_entity: pyiris.ingestion.task.entiry.metadata_entity.MetadataEntity

    :param task_entity: the task definition entity object
    :type task_entity: optional, pyiris.ingestion.task.entity.jdbc_task_entity.JdbcTaskEntity

    :param engine: The processing engine to be used. Defaults to the Spark object.
    :type engine: Optional, pyiris.infrastructure.spark.spark.Spark
    """

    def __init__(
        self,
        task_entity: JdbcTaskEntity,
        metadata_entity: MetadataEntity,
        file_system_config: FileSystemConfig,
        file_writer_engine: FileWriter,
        file_reader: FileReader,
        transform_service: TransformService,
        spark_mapper: Optional[SparkMapper] = None,
        engine: Optional[Spark] = None,
        jdbc_reader: Optional[JdbcReader] = None,
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

        self.jdbc_reader_engine = jdbc_reader or JdbcReader(
            table_id=task_entity.name,
            query=task_entity.query,
            connection_string=task_entity.connection_string,
            user=task_entity.login,
            password=task_entity.password,
            options=task_entity.jdbc_reader_options,
        )

    def source_reader(self) -> DataFrame:
        """
        This method intends to read a table in a jdbc database.

        :return: the dataframe
        :rtype: pyspark.sql.DataFrame
        """

        dataframe = self.jdbc_reader_engine.consume(spark=self.engine)
        return dataframe

    @staticmethod
    def build(
        task_entity: JdbcTaskEntity,
        metadata_entity: MetadataEntity,
        engine: Optional[SparkSession] = None,
    ):
        return JdbcTask(
            task_entity=task_entity,
            metadata_entity=metadata_entity,
            engine=engine,
            file_system_config=JdbcTask.build_file_system_config(task_entity),
            file_writer_engine=JdbcTask.build_file_writer_engine(
                JdbcTask.build_file_system_config(task_entity)
            ),
            file_reader=JdbcTask.build_file_reader(task_entity),
            transform_service=JdbcTask.build_transform_service(task_entity),
        )
