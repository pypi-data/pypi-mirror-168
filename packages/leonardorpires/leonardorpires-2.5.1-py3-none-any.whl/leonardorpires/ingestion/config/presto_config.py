import os
from typing import Optional, Union

from pyspark.sql import DataFrame

from pyiris.infrastructure.common.config import get_key


class PrestoConfig(object):
    """
    This class intends to get configs to write a presto table or just sync an existing table with storage partitions.
    :param format: file format to be read in the data lake
    :type format: string
    :param path: path where the file will be read, without mount name and country
    :type path: string
    :param country: the country path in the data lake
    :type country: string
    :param mount_name: the mount name where is the file
    :type mount_name: string
    :param schema: the schema where will be created the table in the Presto
    :type schema: string
    :param table_name: the name of the table that will be created
    :type table_name: string
    :param partition_by: the name of the partitioning column
    :type partition_by: string or list, optional
    :param sync_mode: the partition sync mode
    :type sync_mode: string, optional
    """

    def __init__(
        self,
        format: str,
        path: str,
        country: str,
        mount_name: str,
        schema: str,
        table_name: str,
        partition_by: Optional[Union[str, list]] = None,
        sync_mode: Optional[list] = None,
    ):
        self.format = format
        self.path = path
        self.country = country
        self.mount_name = mount_name
        self.schema = schema
        self.table_name = table_name
        self.partition_by = partition_by
        self.sync_mode = sync_mode or "FULL"

    def build_drop_table_query(self) -> str:
        """
        This method will always be performed before the create_query
        to ensure that if the table exists, it will be erased so the new
        one can be created in order to update it.
        :return: the Presto SQL command to drop the table
        :rtype: string
        """
        return "DROP TABLE IF EXISTS {schema}.{table_name}".format(
            schema=self.schema, table_name=self.table_name
        )

    def build_create_schema_query(self) -> str:
        # TODO
        # Implement an `external_location` parameter that informs the exact external location of the schema into the data lake. We need to do that because a new version of
        # Hive Metastore requires an external location for schemas.
        # We don't do that yet to avoid refactoring in all pipelines codes that are using that implementation.
        # Now we just get the parent directory of the dataset and assume that it's a table schema.

        schema_path = os.path.split(self.path)[0]
        external_location = "abfss://{mount_name}@{lake_account_name}.dfs.core.windows.net/{country}/{path}".format(
            mount_name=self.mount_name,
            lake_account_name=get_key("lakeAccountName"),
            country=self.country,
            path=schema_path,
        )

        return "CREATE SCHEMA IF NOT EXISTS {schema_name} WITH ( LOCATION = '{external_location}' )".format(
            schema_name=self.schema, external_location=external_location
        )

    def build_create_table_query(self, dataframe: DataFrame) -> str:
        """
        This method will create a Presto SQL query based on the
        read Spark DataFrame
        :param dataframe: the read dataframe to write on the datalake
        :type dataframe: pyspark.sql.dataframe.DataFrame
        :return: the Presto SQL query
        :rtype: string
        """
        column_name_width = 0
        for column in dataframe.columns:
            if len(column) >= column_name_width:
                column_name_width = len(column) + 1

        presto_query = "CREATE TABLE IF NOT EXISTS {schema}.{table} ( \n".format(
            schema=self.schema, table=self.table_name
        )
        for column in dataframe.columns:
            field_delimiter = "\n" if column == dataframe.columns[-1] else ", \n"
            presto_query += (
                column.lower().ljust(column_name_width)
                + self._to_presto_column_type(dict(dataframe.dtypes)[column])
                + field_delimiter
            )

        presto_query += ") \n"
        presto_query += (
            "WITH ( \n"
            "external_location = 'abfss://{}@{}.dfs.core.windows.net/{}/{}', \n".format(
                self.mount_name,
                get_key("lakeAccountName"),
                self.country,
                self.path,
            )
            + "format = 'PARQUET'"
        )

        if self.partition_by is not None:
            if type(self.partition_by) is list:
                presto_query += ", \n" + "partitioned_by = ARRAY{} \n ) \n".format(
                    self.partition_by
                )
            else:
                presto_query += ", \n" + "partitioned_by = ARRAY['{}'] \n ) \n".format(
                    self.partition_by
                )
        else:
            presto_query += ")"

        return presto_query

    def build_sync_schema(self) -> str:
        """
        This method will always be performed if presto config has a partition_by attribute
        to ensure that presto partitions are always synchronized with data lake partitions
        :return: the Presto SQL command to sync table partition
        :rtype: string
        """
        return "CALL system.sync_partition_metadata('{schema}', '{table}', '{sync_mode}')".format(
            schema=self.schema, table=self.table_name, sync_mode=self.sync_mode
        )

    @staticmethod
    def _to_presto_column_type(spark_column_type: str) -> str:
        """
        A helper method to map the desired column type to the equivalent
        Presto column type. It will return the own string if it's not in
        the known Presto types.
        :param spark_column_type: the columns type that will be compared
        :type spark_column_type: string
        :return: The Presto column type
        :rtype: str
        """

        spark_column_type = spark_column_type.lower()
        col_types = {
            "string": "varchar",
            "int": "integer",
            "float": "real",
            "long": "bigint",
            "datetime": "timestamp",
            "time": "varchar",
        }

        if spark_column_type in col_types.keys():
            return col_types[spark_column_type]
        else:
            return spark_column_type
