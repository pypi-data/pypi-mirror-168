from typing import List

from pyspark.sql import DataFrame

from pyiris.infrastructure.spark.spark import Spark
from pyiris.ingestion.extract.readers.file_reader import FileReader


class ExtractService(object):
    """
    This class intends to work as a service. This service gives to the user an way to extract a dataset by using
    a SQL query over file readers objects.

    :param readers: the readers objects
    :type readers: List[pyiris.ingestion.extract.readers.file_reader.FileReader]

    :param query: the SQL query to process the extract
    :type query: string
    """

    def __init__(self, readers: List[FileReader], query: str) -> None:
        self.readers = readers
        self.query = query

    def handler(self, spark: Spark) -> DataFrame:
        """This method intends to execute the extract service by using a given SQL query over the given temp views in the
        readers.

        :param spark: the Spark session used to extract the dataset
        :type spark: optional, pyspark.sql.session.SparkSession

        :return: the dataset result of the query
        :rtype: pyspark.sql.dataframe.DataFrame
        """
        for reader in self.readers:
            reader.build(spark=spark)

        return spark.sql_query(self.query)
