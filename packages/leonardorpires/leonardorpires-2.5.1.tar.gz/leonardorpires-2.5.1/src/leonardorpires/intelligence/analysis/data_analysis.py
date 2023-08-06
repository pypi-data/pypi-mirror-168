import warnings

import databricks.koalas as ks
import pandas as pd
from pyspark.sql import DataFrame

from pyiris.ingestion.utils.utils import DataLimitationWarning

_EDA_FRACTION = 0.05
_DATAFRAME_HEAD_LENGTH = 5
_LIMIT_DATAFRAME_COUNT = 1000000


class DataAnalysis(object):
    """
    This class intends to facilitate the data exploration from Spark Dataframes,
    helping users to maintain a good balance between the flexibility of Pandas
    and the amount of resources used
    """

    def __init__(self, dataframe: DataFrame):
        self.dataframe = dataframe

    def _check_data_length(self, reduced_dataframe: DataFrame) -> None:
        if reduced_dataframe.count() >= _LIMIT_DATAFRAME_COUNT:
            warnings.warn(
                "You are working with the limitation of 1M rows. If you desire to have a larger dataset"
                "procceed working with Spark",
                DataLimitationWarning,
            )
        pass

    # TODO método para limitar o número de linhas utilizadas -> DRY

    # TODO fraction -> para EDA, optional

    def make_eda(self, frac: float = _EDA_FRACTION) -> pd.DataFrame:
        """
        Creating a sampled pandas Dataframe for exploration,
        limiting to work with 1 Million rows at maximum.
        The `_check_data_lenght` method is applied to raise a warning in case
        the user is working with a larger DataFrame.

        :param spark: the Spark session to consume the data
        :type spark: SparkSession

        :param frac: The sample size to fraction the spark DataFrame
        :type frac: float, optional

        :return: The DataFrame, limited to 1 Million rows
        :rtype: pd.DataFrame
        """

        eda_df = self.dataframe.sample(frac).limit(_LIMIT_DATAFRAME_COUNT)
        self._check_data_length(eda_df)

        return eda_df.toPandas()

    # TODO rethink method

    def to_pandas(self) -> pd.DataFrame:
        """
        Transform the spark.DataFrame into a pandas Dataframe,
        limiting to work with 1 Million rows at maximum.
        The `_check_data_lenght` method is applied to raise a warning in case
        the user is working with a larger DataFrame.

        :return: The DataFrame, limited to 1 Million rows
        :rtype: pd.DataFrame
        """

        pandas_dataframe = self.dataframe.limit(_LIMIT_DATAFRAME_COUNT)
        self._check_data_length(pandas_dataframe)

        return pandas_dataframe.toPandas()

    def to_koalas(self) -> ks.frame.DataFrame:
        """
        Transform the spark.DataFrame into a koalas Dataframe for exploration.

        :param spark: the Spark session to consume the data
        :type spark: SparkSession

        :return: The koalas DataFrame
        :rtype: koalas.DataFrame
        """
        return self.dataframe.to_koalas()
