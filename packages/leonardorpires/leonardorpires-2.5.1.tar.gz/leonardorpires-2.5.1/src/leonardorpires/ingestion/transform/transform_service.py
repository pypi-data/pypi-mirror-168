from functools import reduce
from typing import List

from pyspark.sql import DataFrame

from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.transform.transformations.transformation import Transformation

logger = Logger(__name__)


class TransformService(object):
    """This class works as a service to scheduler the transformation jobs.

    :param transformations: a list with the transformations that will be made
    :type transformations: list[Transformations]
    """

    def __init__(self, transformations: List[Transformation]):
        self.transformations = transformations

    @logger.log_decorator
    def handler(self, dataframe) -> DataFrame:
        """This method intends to execute the transformations elencated in the LoadService class.

        :param dataframe: the dataframe that will be transformated
        :type dataframe: pyspark.sql.dataframe.DataFrame

        :return: a transformated dataframe
        :rtype: pyspark.sql.dataframe.DataFrame
        """
        logger.info("Transform service dataframe handler called")
        transformed_dataframe = reduce(
            lambda df, transformation: transformation.transform(df),
            self.transformations,
            dataframe,
        )

        return transformed_dataframe
