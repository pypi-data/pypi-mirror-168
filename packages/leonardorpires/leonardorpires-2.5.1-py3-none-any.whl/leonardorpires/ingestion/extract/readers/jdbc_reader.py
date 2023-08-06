from typing import Optional, Union

from pyspark.sql import DataFrame

from pyiris.infrastructure import Spark
from pyiris.infrastructure.common.exception import (
    JdbcReaderException,
    PyIrisConnectionException,
)
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.extract.readers.reader import Reader
from pyiris.ingestion.validator.jdbc_reader_validator import JdbcReaderValidator

logger = Logger(__name__)


class JdbcReader(Reader):
    """
    This class intends to create a connection with jdbc databases and run a query.
    :param connection_string: the database connections string
    :type connection_string: string
    :param table_id: the database table where the data will be extracted from
    :type table_id: string
    :param query: the arguments validator class
    :type query: optional, pyiris.ingestion.validator.dw_writer_validator.PrestoWriterValidator
    :param user: the database user
    :type user: string
    :param password: the database password
    :type password: string
    :param options: the all other allowed spark read options for jdbc
    :type options: optional, dict
    """

    def __init__(
        self,
        connection_string: str,
        table_id: str,
        password: str,
        user: str,
        query: str,
        options: Optional[dict] = None,
        validator: Optional[JdbcReaderValidator] = None,
    ):
        super().__init__(table_id)
        self.connection_string = connection_string
        self.password = password
        self.user = user
        self.query = query
        self.options = options
        self.validator = validator or JdbcReaderValidator()

    @logger.log_decorator
    def consume(self, spark: Spark) -> Union[DataFrame, ValueError]:
        """
        This method intends to return the database table as a spark dataframe
        :param spark: the class that runs the job
        :type spark: pyiris.infrastructure.spark.spark.Spark
        :return: the intended dataframe
        :rtype: pyspark.sql.DataFrame
        """

        result = self.validator.validate(jdbc_reader=self.__dict__)
        if result.is_right():
            logger.info(
                "Reading Data from table: {}, using user: {}".format(
                    self.table_id, self.user
                )
            )

            try:
                return spark.read_jdbc(
                    url=self.connection_string,
                    query=self.query,
                    user=self.user,
                    password=self.password,
                    options=self.options,
                )

            except Exception as e:
                raise PyIrisConnectionException(message=e)

        else:
            raise JdbcReaderException(
                message=f"Error when try to read from jdbc source. Invalid arguments: {result.value()}"
            )
