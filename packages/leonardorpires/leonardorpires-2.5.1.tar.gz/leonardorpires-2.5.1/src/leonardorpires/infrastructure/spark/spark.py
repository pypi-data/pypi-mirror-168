from typing import List, Optional, Union

from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType

from pyiris.infrastructure.common.config import environment, get_key


class Session(object):
    @staticmethod
    def build():
        if environment == "TEST":
            return SparkSession.builder.config(
                "spark.jars.packages",
                "org.postgresql:postgresql:42.2.10,"
                "io.delta:delta-core_2.12:1.0.0,"
                "com.crealytics:spark-excel_2.12:0.13.8",
            ).getOrCreate()
        else:
            return SparkSession.builder.getOrCreate()


class Spark(object):
    def __init__(self, session: Optional[SparkSession] = None) -> None:
        self.session = session or Session.build()

    def read(self, format: str, path: str, options: Optional[dict] = None) -> DataFrame:
        """
        This method intends to read a spark dataframe.
        :param format: the file format to be read
        :type format: String, required, not null
        :param path: the path with the file in the IRIS environment
        :type path: String, required, not null
        :param options: the spark options to read a file
        :type options: Dict, optional
        :return: a Spark dataframe
        :rtype: pyspark.sql.dataframe.DataFrame
        """
        if options is None:
            options = {}
        return self.session.read.load(path=path, format=format, **options)

    def read_jdbc(
        self,
        url: str,
        query: str,
        user: str,
        password: str,
        options: Optional[dict] = None,
    ) -> DataFrame:
        """
        This method intends to read a spark dataframe.
        :param url: the url used to make the connection with the data warehouse
        :type url: string
        :param query: the spark options to read a file
        :type query: Dict, optional
        :param user: the database user
        :type user: string
        :param password: the database password
        :type password: string
        :param options: the allowed spark extra options
        :type options: dict
        :return: a Spark dataframe
        :rtype: pyspark.sql.dataframe.DataFrame
        """
        if options is None:
            options = {}
        dataframe = self.session.read.load(
            format="jdbc", url=url, query=query, user=user, password=password, **options
        )
        return dataframe

    @staticmethod
    def write(
        dataframe: DataFrame,
        path: str,
        format: str,
        mode: str,
        partition_by: Optional[Union[str, list]] = None,
        options: Optional[dict] = None,
    ) -> None:
        """
        This method is responsible for writing a Spark dataframe as files based on the passed arguments (path, format, mode, partition_by...).
        :param dataframe: the dataframe that will be written
        :type dataframe: pyspark.sql.dataframe.DataFrame
        :param path: the file path where dataframe will be written in the file system
        :type path: string
        :param format: the file format used to written the dataframe
        :type format: string
        :param mode: the write mode used to written the dataframe
        :type mode: string
        :param partition_by: the names of partitioning columns
        :type partition_by: string or list
        :param options: an allowed spark write option
        :type options: dict, options, not null
        """
        if options is None:
            options = {}
        dataframe.write.save(
            path=path, format=format, mode=mode, partitionBy=partition_by, **options
        )

    def sql_query(self, query: str) -> DataFrame:
        """This method intends to return a dataframe result of a SQL query over a given dataframe.
        :param query: the expected query to be applied
        :type query: string
        :raises: ValueError -- Query parameter must be a string!
        :returns: the dataframe result of the query
        :rtype: pyspark.sql.dataframe.DataFrame
        """
        if not isinstance(query, str):
            raise ValueError("Query parameter must be a string!")

        return self.session.sql(query)

    @staticmethod
    def write_dw(
        dataframe: DataFrame,
        url: str,
        table_name: str,
        mode: str,
        temp_path: str,
        temp_container: str,
        options: Optional[dict] = None,
    ) -> None:
        """
        This method intends to create a table or actualize it if exists on DW (Azure Data Warehouse).
        :param dataframe: the Spark dataframe that will be written
        :type dataframe: pyspark.sql.dataframe.DataFrame
        :param url: the url used to make the connection with the data warehouse
        :type url: string
        :param table_name: the name of an existing table that will be actualized, or will be created. Necessarily, this argument has to follow the format "schema.table" and an existing schema has to be passed.
        :type table_name: string
        :param mode: the write mode used to written the dataframe
        :type mode: string
        :param temp_path: the file path where the data will be temporarily stored in the blob, setted based on the environment variables ("BLOB_ACCOUNT_NAME"), during the write process
        :type temp_path: string
        :param temp_container: the name of the container where the data will be stored temporarily
        :type temp_container: string
        :param options: another option accepted by Spark write
        :type options: optional, dict
        """
        if options is None:
            options = {}
        dataframe.write.save(
            format="com.databricks.spark.sqldw",
            mode=mode,
            url=url,
            forwardSparkAzureStorageCredentials="true",
            tempDir="wasbs://{temp_container}@{BLOB_ACCOUNT_NAME}.blob.core.windows.net/{temp_path}".format(
                temp_container=temp_container,
                BLOB_ACCOUNT_NAME=get_key("blobAccountName"),
                temp_path=temp_path,
            ),
            dbTable=table_name,
            **options,
        )

    @staticmethod
    def write_jdbc(
        dataframe: DataFrame,
        url: str,
        table_name: str,
        mode: str,
        truncate: str,
        options: Optional[dict] = None,
    ) -> None:
        """
        This method intends to create a table or actualize it if exists on a SQL database with jdbc connection.
        :param dataframe: the Spark dataframe that will be written
        :type dataframe: pyspark.sql.dataframe.DataFrame
        :param url: the url used to make the connection with the data base
        :type url: string
        :param table_name: the name of an existing table that will be actualized, or will be created. This argument has to follow the format "schema.table" and an existing schema has to be passed.
        :type table_name: string
        :param truncate: option of truncate or not an existing table
        :type truncate: string
        :param mode: the write mode used to write the dataframe
        :type mode: string
        :param options: another options accepted by Spark
        :type: dict, optional
        """
        if options is None:
            options = {}
        dataframe.write.save(
            format="jdbc",
            url=url,
            dbtable=table_name,
            truncate=truncate,
            mode=mode,
            **options,
        )

    def parse_dict_list_to_dataframe(self, schema: dict, data: List[dict]) -> DataFrame:
        """
        This method intends to parse a dict to a spark dataframe.

        :param data: the dict that will become a dataframe
        :type data: list of dicts

        :param schema: the spark schema
        :type schema: dict

        :return: the parsed dataframe
        :rtype: pyspark.sql.DataFrame
        """
        spark_schema = StructType.fromJson(schema)
        return self.session.createDataFrame(data, spark_schema)

    def set_spark_dw_writer_configs(self) -> None:
        """
        This method intends to set "fs.azure.account.key.blob_account_name.blob.core.windows.net" config, in RuntimeConfig :class:pyspark.sql.conf.RuntimeConfig.
        The variable blobAccessKey is obtained from a key vault.
        """
        self.session.conf.set(
            "fs.azure.account.key.{BLOB_ACCOUNT_NAME}.blob.core.windows.net".format(
                BLOB_ACCOUNT_NAME=get_key("blobAccountName")
            ),
            "{BLOB_ACCESS_KEY}".format(BLOB_ACCESS_KEY=get_key("blobAccessKey")),
        )


class SparkExtraConfigs(object):
    def __init__(self, session=None) -> None:
        self.session: Optional[SparkSession] = session or Session.build()

    def unset_spark_config(self) -> None:
        """
        This method intends to unset the Spark session extra configs to be not able to access the Iris Azure Data Lake
        Gen 2 with abfs system and Bifrost Azure Blob Storage with wasbs.
        The variable "lakeAccountName" and "BifrostBlobAccountName" is obtained from a key vault.
        """
        self.session.conf.unset(
            "fs.azure.account.auth.type.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountName")
            )
        )
        self.session.conf.unset(
            "fs.azure.account.oauth.provider.type.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountName")
            )
        )
        self.session.conf.unset(
            "fs.azure.account.oauth2.client.id.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountName")
            )
        )
        self.session.conf.unset(
            "fs.azure.account.oauth2.client.secret.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountName")
            )
        )
        self.session.conf.unset(
            "fs.azure.account.oauth2.client.endpoint.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountName")
            )
        )
        self.session.conf.unset(
            "fs.azure.account.key.{BifrostBlobAccountName}.blob.core.windows.net".format(
                BifrostBlobAccountName=get_key("BifrostBlobAccountName")
            )
        )

    def set_spark_abfs_iris(self) -> None:
        """
        This method intends to set the Spark session extra configs to be able to access the Iris Azure Data Lake Gen 2 (ADLS) with abfs system.
        The variables "lakeAccountName", "IrisLakeSecret", "IrisLakeClientID" and "IrisLakeTenantID" are obtained from a key vault.
        """
        self.session.conf.set(
            "fs.azure.account.auth.type.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountName")
            ),
            "OAuth",
        )
        self.session.conf.set(
            "fs.azure.account.oauth.provider.type.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountName")
            ),
            "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
        )
        self.session.conf.set(
            "fs.azure.account.oauth2.client.id.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountName")
            ),
            get_key("IrisLakeClientID"),
        )
        self.session.conf.set(
            "fs.azure.account.oauth2.client.secret.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountName")
            ),
            get_key("IrisLakeSecret"),
        )
        self.session.conf.set(
            "fs.azure.account.oauth2.client.endpoint.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountName")
            ),
            "https://login.microsoftonline.com/{PYIRIS_TENANT_ID}/oauth2/token".format(
                PYIRIS_TENANT_ID=get_key("IrisLakeTenantID")
            ),
        )

    def set_spark_abfs_iris_private(self) -> None:
        """
        This method intends to set the Spark session extra configs to be able to access the Iris  Azure Data Lake Gen 2 (ADLS) with abfs system.
        The variables "lakeAccountNamePrivate", "IrisLakeSecretPrivate", "IrisLakeClientIDPrivate" and "IrisLakeTenantIDPrivate" are obtained from a key vault.
        """
        self.session.conf.set(
            "fs.azure.account.auth.type.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountNamePrivate")
            ),
            "OAuth",
        )
        self.session.conf.set(
            "fs.azure.account.oauth.provider.type.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountNamePrivate")
            ),
            "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
        )
        self.session.conf.set(
            "fs.azure.account.oauth2.client.id.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountNamePrivate")
            ),
            get_key("IrisLakeClientIDPrivate"),
        )
        self.session.conf.set(
            "fs.azure.account.oauth2.client.secret.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountNamePrivate")
            ),
            get_key("IrisLakeSecretPrivate"),
        )
        self.session.conf.set(
            "fs.azure.account.oauth2.client.endpoint.{LAKE_ACCOUNT_NAME}.dfs.core.windows.net".format(
                LAKE_ACCOUNT_NAME=get_key("lakeAccountNamePrivate")
            ),
            "https://login.microsoftonline.com/{PYIRIS_TENANT_ID}/oauth2/token".format(
                PYIRIS_TENANT_ID=get_key("IrisLakeTenantIDPrivate")
            ),
        )

    def set_spark_abfs_brewdat(self) -> None:
        """
        This method intends to set the Spark session extra configs to be able to access the Brewdat Azure Data Lake Gen 2 (ADLS) with abfs system.
        The variables "IrisBrewdatAccountName", "IrisBrewdatSecret", "IrisBrewdatClientId" and "IrisBrewdatTenantId" are obtained from a key vault.
        """
        self.session.conf.set(
            "fs.azure.account.auth.type.{BREWDAT_ACCOUNT_NAME}.dfs.core.windows.net".format(
                BREWDAT_ACCOUNT_NAME=get_key("IrisBrewdatAccountName")
            ),
            "OAuth",
        )
        self.session.conf.set(
            "fs.azure.account.oauth.provider.type.{BREWDAT_ACCOUNT_NAME}.dfs.core.windows.net".format(
                BREWDAT_ACCOUNT_NAME=get_key("IrisBrewdatAccountName")
            ),
            "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
        )
        self.session.conf.set(
            "fs.azure.account.oauth2.client.id.{BREWDAT_ACCOUNT_NAME}.dfs.core.windows.net".format(
                BREWDAT_ACCOUNT_NAME=get_key("IrisBrewdatAccountName")
            ),
            get_key("IrisBrewdatClientId"),
        )
        self.session.conf.set(
            "fs.azure.account.oauth2.client.secret.{BREWDAT_ACCOUNT_NAME}.dfs.core.windows.net".format(
                BREWDAT_ACCOUNT_NAME=get_key("IrisBrewdatAccountName")
            ),
            get_key("IrisBrewdatSecret"),
        )
        self.session.conf.set(
            "fs.azure.account.oauth2.client.endpoint.{BREWDAT_ACCOUNT_NAME}.dfs.core.windows.net".format(
                BREWDAT_ACCOUNT_NAME=get_key("IrisBrewdatAccountName")
            ),
            "https://login.microsoftonline.com/{BREWDAT_TENANT_ID}/oauth2/token".format(
                BREWDAT_TENANT_ID=get_key("IrisBrewdatTenantId")
            ),
        )

    def set_spark_wasbs_analyticsplatformblob(self) -> None:
        """
        This method intends to set the Spark session extra configs to be able to access the analyticsplatformblob Azure Blob Storage with wasbs system.
        The variables "blobAccountName" and "blobAccessKey" are obtained from a key vault.
        """
        self.session.conf.set(
            "fs.azure.account.key.{blobAccountName}.blob.core.windows.net".format(
                blobAccountName=get_key("blobAccountName")
            ),
            get_key("blobAccessKey"),
        )

    def set_spark_wasbs_bifrost(self) -> None:
        """
        This method intends to set the Spark session extra configs to be able to access the Bifrost Azure Blob Storage with wasbs system.
        The variables "BifrostBlobAccountName" and "BifrostBlobAccessKey" are obtained from a key vault.
        """
        self.session.conf.set(
            "fs.azure.account.key.{BifrostBlobAccountName}.blob.core.windows.net".format(
                BifrostBlobAccountName=get_key("BifrostBlobAccountName")
            ),
            get_key("BifrostBlobAccessKey"),
        )
