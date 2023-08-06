from pyspark.sql.functions import expr

from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.transform.transformations.transformation import Transformation

logger = Logger(__name__)


class SqlTransformation(Transformation):
    """This class intends to make a SQL transformation in a given dataframe.

    :param name: the name of transform operation
    :type name: string

    :param description: the description of the transformation
    :type description: string

    :param to_column: the name of the result column
    :type to_column: string

    :param sql_expression: the SQL expression that intends to be operated
    :type sql_exspression: string
    """

    def __init__(
        self, name: str, description: str, to_column: str, sql_expression: str
    ):
        super().__init__(name, description)
        self.name = name
        self.description = description
        self.to_column = to_column
        self.sql_expression = sql_expression

    @logger.log_decorator
    def transform(self, dataframe):
        """This method intends to execute the given transformation in the SqlTransformation instance.

        :param dataframe: the dataframe that will be transformated
        :type dataframe: pyspark.sql.dataframe.DataFrame

        :return: the transformed dataframe
        :rtype: pyspark.sql.dataframe.DataFrame
        """
        return dataframe.withColumn(self.to_column, expr(self.sql_expression))
