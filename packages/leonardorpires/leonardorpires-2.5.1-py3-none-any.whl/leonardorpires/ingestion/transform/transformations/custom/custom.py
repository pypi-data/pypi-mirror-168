from typing import Any, Optional

from pyspark.sql import DataFrame
from pyspark.sql import functions as f

from pyiris.infrastructure.common.helper import Helper


def multiply(dataframe, to_column, column1, column2):
    dataframe = dataframe.withColumn(to_column, f.col(column1) * f.col(column2))
    return dataframe


def divide(dataframe, to_column, column1, column2):
    dataframe = dataframe.withColumn(to_column, f.col(column1) / f.col(column2))
    return dataframe


def add(dataframe, to_column, column1, column2):
    dataframe = dataframe.withColumn(to_column, f.col(column1) + f.col(column2))
    return dataframe


def subtract(dataframe, to_column, column1, column2):
    dataframe = dataframe.withColumn(to_column, f.col(column1) - f.col(column2))
    return dataframe


def uppercase_column_names(dataframe):
    col_names = dataframe.schema.names
    for name in col_names:
        dataframe = dataframe.withColumnRenamed(name, name.upper())
    return dataframe


def drop_duplicate(
    dataframe: DataFrame,
    exclude_only: Optional[list] = None,
    based_on_columns: Optional[list] = None,
    enable: Optional[Any] = True,
) -> DataFrame:
    """
    This function intends to drop duplicated lines based on inputted columns or excluded columns. If 'exclude_only'
    parameter is passed, the drop function will compare lines of the columns not excluded. Else, if param
    'based_on_columns' is passed, only these columns are considered on the drop. So, just one param can be passed; if
    both are passed, the function will consider only 'exclude_only'. In the other hand, if no argument is passed, all columns
    are considered on the drop comparison.

    :param dataframe: the dataframe that will have lines dropped
    :type dataframe: pyspark.sql.dataframe.DataFrame

    :param exclude_only: the columns excluded on the line comparations
    :type exclude_only: optional, list

    :param enable: the transformation status
    :type enable: optional, True or False

    :param based_on_columns: the columns for the comparison
    :type based_on_columns: optional, list

    :return: the resulting dataframe
    :rtype: pyspark.sql.dataframe.DataFrame
    """
    if enable:
        columns = dataframe.columns
        if exclude_only:
            columns = [item for item in columns if item not in exclude_only]
        elif based_on_columns:
            columns = based_on_columns

        return dataframe.dropDuplicates(columns)
    else:
        return dataframe


def add_ingestion_date(dataframe: DataFrame, enable: Optional[Any] = True) -> DataFrame:
    """
    This function intends to add a control column with the ingestion date per dataframe line.

    :param dataframe: the dataframe that will have the control column added.
    :type dataframe: pyspark.sql.dataframe.DataFrame

    :param enable: the transformation status
    :type enable: optional, True or False

    :return: the resulting dataframe
    :rtype: pyspark.sql.dataframe.DataFrame
    """
    if enable:
        year = dataframe.withColumn("year", f.year(f.current_date()))
        month = year.withColumn("month", f.month(f.current_date()))
        return month.withColumn("day", f.dayofmonth(f.current_date()))
    else:
        return dataframe


def capitalize_first_letter(word):
    if word:
        word = list(word)
        word[0] = word[0].capitalize()
        word = "".join(word)
    return word


def snakecase_column_names(
    dataframe: DataFrame, enable: Optional[Any] = True
) -> DataFrame:
    """
    This method intends to rename all columns of a given dataframe to snake case.

    The transformations applied are:
    - replacing letters containing accents and special characters (e.g. replacing 'á', 'à', 'ã' or 'â' to 'a');
    - replacing uppercase letters with underscore and lowercase;
    - removing duplicated undescore;
    - removing leading and trailing undescore;
    - removing all characters that are not allowed (a-z0-9_)

    :param dataframe: the dataframe that will be transformated
    :type dataframe: pyspark.sql.dataframe.DataFrame

    :param enable: the transformation status
    :type enable: optional, True or False

    :return: the resulting dataframe
    :rtype: pyspark.sql.dataframe.DataFrame
    """
    if enable:
        transformed_dataframe = dataframe
        for column in dataframe.columns:
            transformed_dataframe = transformed_dataframe.withColumnRenamed(
                column, Helper.snake_case(column)
            )
        return transformed_dataframe
    else:
        return dataframe
