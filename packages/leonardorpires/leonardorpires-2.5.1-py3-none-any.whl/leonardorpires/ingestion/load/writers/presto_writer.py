from typing import Optional

from pyspark.sql import DataFrame

from pyiris.infrastructure import Presto
from pyiris.infrastructure.common.exception import PrestoWriterValidatorException
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.config.presto_config import PrestoConfig
from pyiris.ingestion.enums.enums import WriterPriority
from pyiris.ingestion.load.writers.writer import Writer
from pyiris.ingestion.validator.presto_writer_validator import PrestoWriterValidator

logger = Logger(__name__)


class PrestoWriter(Writer):
    """
    This class will create a Presto SQL query based on the constructor's desired table information. It may be that a new
    table is created, or a new sync partition in a existing presto table. It requires an available table in the IRIS
    DataLake with the standard parquet files format and path.
    :param config: the config to create the table
    :type config: pyiris.ingestion.config.presto_config.PrestoConfig
    :param engine: the presto writer executer
    :type engine: pyiris.infrastructure.presto.presto.Presto
    :param priority: the priority order to execute the writers
    :type priority: optional, integer
    :param validator: the arguments validator class
    :type validator: optional, pyiris.ingestion.validator.dw_writer_validator.PrestoWriterValidator
    """

    def __init__(
        self,
        config: PrestoConfig,
        engine: Optional[Presto] = None,
        priority: Optional[int] = None,
        validator: Optional[PrestoWriterValidator] = None,
    ):
        super().__init__(priority, engine)
        self.config = config
        self.engine = engine or Presto()
        self.priority = priority or WriterPriority.PRESTOWRITER.value
        self.validator = validator or PrestoWriterValidator()

    @logger.log_decorator
    def write(self, dataframe: DataFrame) -> None:
        """
        A method to create a string-formatted Presto query after the
        PrestoWriter object has been instantiated.
        :return: The formatted Presto query
        :rtype: str
        """
        result = self.validator.validate(self.config.__dict__)
        if result.is_right() and self.config.sync_mode == "FULL":
            drop_table = self.config.build_drop_table_query()
            self.engine.write(command=drop_table)
            logger.info(f"Dropped table {self.config.table_name}")

        if result.is_right():
            create_schema = self.config.build_create_schema_query()
            self.engine.write(command=create_schema)
            logger.info(f"Created schema {self.config.schema}")

            create_table = self.config.build_create_table_query(dataframe=dataframe)
            self.engine.write(command=create_table)
            logger.info(f"Created table {self.config.table_name}")

            if self.config.partition_by:
                sync_table = self.config.build_sync_schema()
                self.engine.write(command=sync_table)

        else:
            message = f"Error when try to write the files in the path. Invalid parameters: {result.value()}"
            raise PrestoWriterValidatorException(message=message)
