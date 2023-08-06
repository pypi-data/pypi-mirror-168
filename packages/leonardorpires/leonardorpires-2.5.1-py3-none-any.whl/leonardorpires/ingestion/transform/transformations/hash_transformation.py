from typing import List

from pyspark.sql.functions import sha2
from pyspark.sql.types import StringType

from pyiris.infrastructure.common.exception import HashTransformationException
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.transform.transformations.transformation import Transformation

logger = Logger(__name__)


class HashTransformation(Transformation):
    """This class intends to make a hash transformation in a given dataframe.

    :param name: the name of transform operation
    :type name: string

    :param description: the description of the transformation
    :type description: string

    :param from_columns: the list of the columns that will be transformed
    :type from_columns: list[string]
    """

    def __init__(self, name: str, description: str, from_columns: List[str]):
        super().__init__(name, description)
        self.name = name
        self.description = description
        self.from_columns = from_columns

    @logger.log_decorator
    def transform(self, dataframe):
        """This method intends to execute the given transformation in the HashTransformation instance.

        :param dataframe: the dataframe that will be transformated
        :type dataframe: pyspark.sql.dataframe.DataFrame

        :raises: ValueError -- Invalid Spark type! Allowed type: StringType

        :return: the transformed dataframe
        :rtype: pyspark.sql.dataframe.DataFrame
        """
        if self.from_columns is None:
            return dataframe
        else:
            logger.info("Hash Transformation executed successfully!")
            for column in self.from_columns:
                hash_column = column + "_hash"
                if not isinstance(dataframe.schema[column].dataType, StringType):
                    raise HashTransformationException(
                        message="Invalid Spark type! Allowed type: StringType"
                    )

                dataframe = dataframe.withColumn(
                    hash_column, sha2(dataframe[column], 256)
                )

            transformed_dataframe = dataframe.drop(*self.from_columns)
            return transformed_dataframe
