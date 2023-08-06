from typing import Optional

from pyspark.sql import DataFrame

from pyiris.infrastructure.common.config import get_key
from pyiris.infrastructure.common.exception import FileWriterValidatorException
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.spark.spark import Spark, SparkExtraConfigs
from pyiris.ingestion.config.file_system_config import FileSystemConfig
from pyiris.ingestion.enums.enums import WriterPriority
from pyiris.ingestion.load.writers.writer import Writer
from pyiris.ingestion.validator.file_writer_validator import FileWriterValidator

logger = Logger(__name__)


class FileWriter(Writer):
    """
    This class intends to write files in the data lake based on a spark dataframe.

    :param config: the config to create the table
    :type config: pyiris.ingestion.config.file_system_config.FileSystemConfig

    :param engine: the Spark session
    :type engine: optional, pyiris.infrastructure.spark.spark.Spark

    :param validator: the arguments validator class
    :type validator: optional, pyiris.ingestion.validate.file_writer_validator.FileWriterValidator

    :param priority: the priority order to execute the writers
    :type priority: optional, integer

    :param extra_configs_engine: protocol extra configs executor
    :type extra_configs_engine: :class:pyiris.infrastructure.spark.spark.SparkExtraConfigs
    """

    def __init__(
        self,
        config: FileSystemConfig,
        engine: Optional[Spark] = None,
        validator: Optional[FileWriterValidator] = None,
        priority: Optional[int] = None,
        extra_configs_engine: Optional[SparkExtraConfigs] = None,
    ):
        super().__init__(priority, engine)
        self.config = config
        self.engine = engine or Spark()
        self.extra_configs_engine = extra_configs_engine or SparkExtraConfigs()
        self.priority = priority or WriterPriority.FILEWRITER.value
        self.validator = validator or FileWriterValidator()

    @logger.log_decorator
    def write(self, dataframe: DataFrame):
        """
        The write method is responsible for write the files in the data lake. To write, the method use another
        :class:pyiris.ingestion.validator.file_writer_validator.FileWriterValidator to validade the parameters of write.
        To know the validator, acess the FileWriterValidator documentation.
        If the validator do not validate the parameters, an exception with the error value is raised.

        :param dataframe: the dataframe that will be written
        :type dataframe: pyspark.sql.DataFrame

        :raises: Exception -- Error value

        """
        result = self.validator.validate(file_writer=self.config.__dict__)
        if result.is_right():
            logger.info("Writing files in the path: {}".format(self.config.full_path))
            logger.info(
                f"Using format to write: {self.config.format}, mode: {self.config.mode}, and the options: {self.config.options}"
            )
            self.engine.write(
                dataframe=dataframe,
                path=self.config.full_path,
                format=self.config.format,
                mode=self.config.mode,
                partition_by=self.config.partition_by,
                options=self.config.options,
            )

            if get_key("ENVIRONMENT") != "TEST":
                self.extra_configs_engine.unset_spark_config()
                logger.info("The spark config was unset")
        else:
            message = f"Error when try to write the files in the path. Invalid parameters: {result.value()}"
            raise FileWriterValidatorException(message=message)
