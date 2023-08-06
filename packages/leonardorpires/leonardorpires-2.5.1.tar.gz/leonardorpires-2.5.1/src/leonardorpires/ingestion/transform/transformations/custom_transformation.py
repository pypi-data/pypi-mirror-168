from collections.abc import Callable

from pyspark.sql import DataFrame

from pyiris.ingestion.transform.transformations.transformation import Transformation


class CustomTransformation(Transformation):
    """This class intends to be a tool for the user to make custom transformations.

    :param name: the name of the transformation
    :type name: string

    :param description: the transformation description
    :type descriptions: string

    :param method: the custom transformation
    :type method: Callable
    """

    def __init__(self, name: str, description: str, method: Callable, **kwargs):
        super().__init__(name, description)
        self.name = name
        self.description = description
        self.method = method
        self.kwargs = kwargs

    def transform(self, dataframe: DataFrame) -> DataFrame:
        """This method intends to execute the given transformation in the CustomTransformation instance.

        :param dataframe: the dataframe that will be transformated
        :type dataframe: pyspark.sql.dataframe.DataFrame

        :return: the transformated dataframe
        :rtype: pyspark.sql.dataframe.DataFrame
        """
        dataframe = self.method(dataframe, **self.kwargs)
        return dataframe
