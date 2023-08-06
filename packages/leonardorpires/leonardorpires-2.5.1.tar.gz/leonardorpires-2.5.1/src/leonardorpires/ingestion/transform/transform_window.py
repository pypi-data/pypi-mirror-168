from typing import Any

from pyspark.sql import Window, WindowSpec


class TransformWindow(object):
    """
    This class intends to return a Transformation Window Definition with Specification. It helps us define and use
    Window transformations along with the :class:pyiris.ingestion.transformation.SparkTransformation object.

    The user might define a TransformWindow object and then call a desired method to build TransformWindow and return the name and specification, such as:

    ```python
    simple_window = TransformWindow.build(
                        window_name="simple_window",
                        partition_by="some_column",
                        order_by=None or "other_column",
                        upper_bound=4,
                        lower_bound=0
                        )

    range_window = TransformWindow.build_with_range(
                        window_name="range_window",
                        partition_by="some_column",
                        order_by="other_column",
                        upper_bound=4,
                        lower_bound=0
                        )

    rows_window = TransformWindow.build_with_rows(
                        window_name="rows_window",
                        partition_by="some_column",
                        order_by="other_column",
                        upper_bound=4,
                        lower_bound=0
                        )

    windows_list = [simple_window, range_window, rows_window]
    ```
    """

    def __init__(self, name: str, spec: WindowSpec = None):
        self.name = name
        self.spec = spec

    @staticmethod
    def build(name: str, partition_by: Any, order_by: Any = None):
        """
        This class intend to build a simple TransformWindow Specification with partition and order by only.
        When working with Aggregate functions, we don’t need to use order by clause.

        :param name: The desired window name,
        :type name: str

        :param partition_by: the column or list of columns by which the DataFrame should be partitioned
        :type partition_by: str, :class:`Column` or list

        :param order_by: the column or list of columns by which the DataFrame should be ordered.
        :type order_by: str, :class:`Column` or list
        """
        window_spec = Window.partitionBy(partition_by)

        if order_by:
            window_spec.orderBy(order_by)

        return TransformWindow(name=name, spec=window_spec)

    @staticmethod
    def build_with_range(
        name: str,
        partition_by: Any,
        lower_bound: int,
        upper_bound: int,
        order_by: Any = None,
    ):
        """
        This class intend to build a range between TransformWindow Specification.

        :param name: The desired window name,
        :type name: str

        :param partition_by: the column or list of columns by which the DataFrame should be partitioned
        :type partition_by: str, :class:`Column` or list

        :param order_by: the column or list of columns by which the DataFrame should be ordered.
        :type order_by: str, :class:`Column` or list

        :param lower_bound: The inclusive Window boundary start
        :type lower_bound: int

        :param upper_bound: The inclusive Window boundary end
        :type upper_bound: int

        """

        window_spec = Window.partitionBy(partition_by)

        if order_by:
            window_spec.orderBy(order_by)

        return TransformWindow(
            name=name,
            spec=Window.partitionBy(partition_by)
            .orderBy(order_by)
            .rangeBetween(lower_bound, upper_bound),
        )

    @staticmethod
    def build_with_rows(
        name: str,
        partition_by: Any,
        lower_bound: int,
        upper_bound: int,
        order_by: Any = None,
    ):
        """
        This class intend to build a rows between TransformWindow Specification.

        :param name: The desired window name,
        :type name: str

        :param partition_by: the column or list of columns by which the DataFrame should be partitioned
        :type partition_by: str, :class:`Column` or list

        :param order_by: the column or list of columns by which the DataFrame should be ordered.
        :type order_by: str, :class:`Column` or list

        :param lower_bound: The inclusive Window boundary start
        :type lower_bound: int

        :param upper_bound: The inclusive Window boundary end
        :type upper_bound: int

        """

        window_spec = Window.partitionBy(partition_by)

        if order_by:
            window_spec.orderBy(order_by)

        return TransformWindow(
            name=name,
            spec=Window.partitionBy(partition_by).rowsBetween(lower_bound, upper_bound),
        )
