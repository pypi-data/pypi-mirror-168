from abc import ABC, abstractmethod
from typing import Optional, Union

from pyspark.sql import DataFrame

from pyiris.infrastructure.common.helper import Helper
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.spark.spark import Spark

logger = Logger(__name__)


class Reader(ABC):
    """
    This class is responsible for structuring the readers.The methods are responsible for giving the tools to
    make a reader.

    :param table_id: the given id for the table that will be used to refer it in the temp view
    :type table_id: string
    """

    def __init__(
        self, table_id, helper: Optional[Helper] = None, base_path: Optional[str] = None
    ):
        self.table_id = table_id
        self.helper = helper or Helper()
        self.base_path = base_path

    @property
    def base_path(self) -> Union[str, None]:
        return self._base_path

    @base_path.setter
    def base_path(self, value) -> None:
        if value is None:
            self._base_path = self.helper.get_base_path()
        else:
            self._base_path = value

    @logger.log_decorator
    def build(self, spark: Spark):
        """
        This methods intend to read a dataset and create a temp view from the dataset.
        It was idealized to give for the user an way to use the Sql tools of extracting in a temp view.

        :param spark: the Spark session used to extract the dataset
        :type spark: optional, pyspark.sql.session.SparkSession
        """
        transformed_dataframe = self.consume(spark=spark)
        transformed_dataframe.createOrReplaceTempView(self.table_id)
        logger.info(f"The temporary view {self.table_id} was created")

    @abstractmethod
    def consume(self, spark: Spark) -> DataFrame:
        """
        This method intend to consume a dataset with Spark and return a dataframe.

        :param spark: the Spark session used to extract the dataset
        :type spark: pyspark.sql.session.SparkSession
        """
        pass
