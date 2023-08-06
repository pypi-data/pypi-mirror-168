from typing import Optional, Union

from pyspark.sql.dataframe import DataFrame

from pyiris.infrastructure.common.exception import SqlWriterValidatorException
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.spark.spark import Spark
from pyiris.ingestion.config.dm_config import DmWriterConfig
from pyiris.ingestion.config.dw_config import DwWriterConfig
from pyiris.ingestion.enums.enums import WriterPriority
from pyiris.ingestion.load.writers.writer import Writer
from pyiris.ingestion.validator.sql_writer_validator import SqlWriterValidator

logger = Logger(__name__)


class SqlWriter(Writer):
    """
    This class intends to create or update a table in the Azure Data Warehouse or Microsoft Sql Server based on
    the parameters passed in the object DwWriterConfig or DmWriterConfig. It requires an existent schema in the SQL
    database.

    :param config: the config to create the table
    :type config: pyiris.ingestion.config.dw_config.DwWriterConfig or pyiris.ingestion.config.dm_config.DmWriterConfig

    :param engine: the Spark session
    :type engine: optional, pyiris.infrastructure.spark.spark.Spark

    :param validator: the arguments validator class
    :type validator: optional, pyiris.ingestion.validator.sql_writer_validator.SqlWriterValidator

    :param priority: the priority order to execute the writers
    :type priority: optional, integer
    """

    def __init__(
        self,
        config: Union[DwWriterConfig, DmWriterConfig],
        engine: Optional[Spark] = None,
        validator: Optional[SqlWriterValidator] = None,
        priority: Optional[int] = None,
    ):
        super().__init__(priority, engine)
        self.config = config
        self.engine = engine or Spark()
        self.validator = validator or SqlWriterValidator()
        self.priority = priority or WriterPriority.DWWRITER.value

    @logger.log_decorator
    def write(self, dataframe: DataFrame) -> None:
        """
        The write method is responsible for writing the table. It uses another class
        :class:pyiris.ingestion.validator.sql_writer_validator.SqlWriterValidator to validate the parameters of write.
        To know the validator, access the respective class documentation.
        If the validator doesn't validate the parameters, an exception with the error value is raised.

        :param dataframe: the dataframe that will be written
        :type dataframe: pyspark.sql.dataframe.DataFrame

        :raises: Exception -- Error value
        """
        result = self.validator.validate(sql_params=self.config.__dict__)
        if result.is_right() and self.config.type == "dw_writer":
            self.engine.set_spark_dw_writer_configs()
            self.engine.write_dw(
                dataframe=dataframe,
                url=self.config.get_url(),
                table_name=self.config.get_table_name(),
                mode=self.config.mode,
                temp_path=self.config.temp_path,
                temp_container=self.config.temp_container,
                options=self.config.options,
            )
            logger.info(
                "The table in the DW {} was written successfully".format(
                    self.config.get_table_name()
                )
            )
        elif result.is_right() and self.config.type == "jdbc":
            self.engine.write_jdbc(
                dataframe=dataframe,
                url=self.config.get_url(),
                table_name=self.config.get_table_name(),
                mode=self.config.mode,
                truncate=self.config.truncate,
                options=self.config.options,
            )
            logger.info(
                "The table in the Jdbc {} was written successfully".format(
                    self.config.get_table_name()
                )
            )
        else:
            logger.error("Sql Write Parameters Error: {}".format(result.value()))
            raise SqlWriterValidatorException()
