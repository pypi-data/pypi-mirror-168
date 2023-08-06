from functools import reduce
from typing import Callable, List, Optional

from pyspark.sql import DataFrame

from pyiris.infrastructure.common.exception import SparkTransformationException
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.transform.transform_window import TransformWindow
from pyiris.ingestion.transform.transformations.transformation import Transformation

logger = Logger(__name__)


class SparkTransformation(Transformation):
    """
    This class will make a list of Spark transformations, given a list of
    transformation functions. It can either be something from pyspark.sql.functions
    module or a Spark UDF.

    All of the operations will happen for a given column. If the user intends to make the
    same operations for two different columns, they should build two SparkTransformation
    objects.

    Since it inherits from :class:`pyiris.ingestion.transform.Transformation, the user should
    always provide a name and description for the transformations they are making.

    :param name: the transformation name
    :type name: str

    :param description: the description of what you intend to do
    :type description: str

    :param from_column: the name of the column from which the transformations will be applied
    :type from_column: str

    :param functions: a list of all of the functions to be applied to the given column
    :type functions: List[Callable]

    :param windows: A list of Window Specifications for aggregated transformations
    :type windows: :class:WindowSpec

    """

    def __init__(
        self,
        name: str,
        description: str,
        from_column: str,
        functions: List[Callable],
        windows: List[TransformWindow] = None,
    ):
        super().__init__(name=name, description=description)
        self.from_column = from_column
        self.functions = functions
        self.windows = windows

    @logger.log_decorator
    def transform(self, dataframe) -> DataFrame:
        """
        This method will apply the given Spark transformations to the dataframe that
        is injected to it.
        """
        try:
            if self.windows:
                for window_object in self.windows:
                    for function in self.functions:
                        dataframe = dataframe.withColumn(
                            self._build_transformed_column_name(
                                function=function, window_name=window_object.name
                            ),
                            function(self.from_column).over(window_object.spec),
                        )
            else:
                dataframe = reduce(
                    lambda df, func: df.withColumn(
                        self._build_transformed_column_name(func),
                        func(self.from_column),
                    ),
                    self.functions,
                    dataframe,
                )
        except Exception as e:
            raise SparkTransformationException(message=e)

        return dataframe

    def _build_transformed_column_name(
        self, function, window_name: Optional[str] = None
    ) -> str:
        """
        This is a private helper method that takes in a function and returns a string with the
        concatenated name the transformed column will have
        """
        function_name = getattr(function, "__name__", repr(function))
        new_column_name = self.from_column + "__" + function_name

        if window_name:
            new_column_name = new_column_name + "__window_" + window_name

        return new_column_name
