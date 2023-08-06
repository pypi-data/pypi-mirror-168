from typing import List

from pyspark.sql import DataFrame

from pyiris.ingestion.load.writers.writer import Writer


class LoadService(object):
    """
    This class works as a service to scheduler the load jobs.

    :param writers: a list with the writers that have to be executed
    :type writers: list
    """

    def __init__(self, writers: List[Writer]) -> None:
        self.writers = writers

    def commit(self, dataframe: DataFrame) -> None:
        """
        This method intends to execute the writers inputted in the LoadService class.

        :param dataframe: the dataframe that will be written
        :type dataframe: pyspark.sql.dataframe.DataFrame
        """
        self.writers.sort(key=lambda writer: writer.priority)
        for writer in self.writers:
            writer.write(dataframe=dataframe)
