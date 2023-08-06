from abc import abstractmethod
from typing import List, Optional

from pyspark.sql import DataFrame
from pyspark.sql.utils import AnalysisException

from pyiris.infrastructure import Spark
from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.spark.spark_mapper import SparkMapper
from pyiris.ingestion.config.file_system_config import FileSystemConfig
from pyiris.ingestion.enums.enums import IrisMountNames
from pyiris.ingestion.extract import FileReader
from pyiris.ingestion.load import FileWriter
from pyiris.ingestion.task.base_task import BaseTask
from pyiris.ingestion.task.entity.task_entity import TaskEntity
from pyiris.ingestion.transform.transform_builder import SourceTransformBuilder
from pyiris.ingestion.transform.transform_service import TransformService

logger = Logger(__name__)


class SourceTask(BaseTask):
    """
    This class intends to define a base to source etl tasks.

    :param metadata_entity: the dataset metadata object
    :type metadata_entity: pyiris.ingestion.task.entiry.metadata_entity.MetadataEntity

    :param task_entity: the task definition entity object
    :type task_entity: optional, pyiris.ingestion.task.entity.task_entity.TaskEntity

    :param spark_mapper: The Spark mapper object.
    :type spark_mapper: Optional, pyiris.infrastructure.spark.spark_mapper.SparkMapper

    :param engine: The processing engine to be used. Defaults to the Spark object.
    :type engine: Optional, pyiris.infrastructure.spark.spark.Spark

    :param file_system_config: The File System config object.
    :type file_system_config: Optional, pyiris.ingestion.config.file_system_config.FileSystemConfig

    :param file_writer_engine: The file writer object.
    :type file_writer_engine: Optional, pyiris.ingestion.load.FileWriter

    :param file_reader: The file reader object.
    :type file_reader: Optional, pyiris.ingestion.extract.FileReader

    :param transform_service: The transformations service object.
    :type transform_service: Optional, pyiris.ingestion.transform.transform_service.TransformService

    """

    def __init__(
        self,
        task_entity: TaskEntity,
        metadata_entity: MetadataEntity,
        file_system_config: FileSystemConfig,
        file_writer_engine: FileWriter,
        file_reader: FileReader,
        transform_service: TransformService,
        engine: Optional[Spark] = None,
        spark_mapper: Optional[SparkMapper] = None,
    ):
        super().__init__(
            task_entity,
            metadata_entity,
            file_system_config,
            file_writer_engine,
            file_reader,
            transform_service,
            engine,
            spark_mapper,
        )

        self.task_entity = task_entity
        self.metadata_entity = metadata_entity
        self.source_transform_builder = SourceTransformBuilder()

    @staticmethod
    @abstractmethod
    def build(task_entity: TaskEntity, metadata_entity: MetadataEntity):
        pass

    @logger.log_decorator
    def definitions(self) -> DataFrame:
        """
        This method intends to define the etl tasks. If the extracted dataframe is empty, it will not be processed.
        """
        source_dataframe = self.source_reader()
        if not source_dataframe.rdd.isEmpty():
            raw_dataframe = self._raw_definitions(dataframe=source_dataframe)
            return self._trusted_definitions(raw_dataframe=raw_dataframe)

    @logger.log_decorator
    def source_reader(self) -> DataFrame:
        pass

    @logger.log_decorator
    def file_writer(self, dataframe: DataFrame) -> None:
        pass

    @logger.log_decorator
    def parse_dataframe(self, data: List[dict]) -> DataFrame:
        """
        This method intends to parse a dataframe from a list of dicts and a schema based on metadata parameter.

        return: the spark dataframe
        rtype: DataFrame
        """

        schema = self.spark_mapper.get_schema_definition(
            metadata=self.metadata_entity.__dict__
        )
        dataframe = self.engine.parse_dict_list_to_dataframe(data=data, schema=schema)
        return dataframe

    @logger.log_decorator
    def _raw_definitions(self, dataframe: DataFrame):
        zone = IrisMountNames.RAWZONE.value
        raw_transformations = self.source_transform_builder.build(
            context=self.task_entity.__dict__, zone=zone
        )
        self.transform_service.transformations = raw_transformations.transformations
        raw_dataframe = self.transform_service.handler(dataframe=dataframe)

        self.file_system_config.mount_name = zone
        self.file_writer_engine.config = self.file_system_config
        self.file_writer_engine.write(dataframe=raw_dataframe)
        return raw_dataframe

    @logger.log_decorator
    def _trusted_definitions(self, raw_dataframe: DataFrame) -> DataFrame:
        zone = IrisMountNames.TRUSTEDZONE.value
        try:
            self.file_reader.table_id = f"{self.task_entity.name}_trusted_dataframe"
            self.file_reader.mount_name = zone

            trusted_dataframe = self.file_reader.consume(spark=self.engine)
            dataframe = trusted_dataframe.union(raw_dataframe)
        except AnalysisException:
            dataframe = raw_dataframe

        trusted_transformations = self.source_transform_builder.build(
            context=self.task_entity.__dict__, zone=zone
        )
        self.transform_service.transformations = trusted_transformations.transformations
        trusted_dataframe = self.transform_service.handler(dataframe=dataframe)

        self.file_system_config.mount_name = zone
        self.file_writer_engine.config = self.file_system_config
        self.file_writer_engine.write(dataframe=trusted_dataframe)
        return trusted_dataframe
