from typing import Optional

from pyiris.infrastructure.common.config import get_key


class DwWriterConfig(object):
    """
    This class intends to get configs to write an ambevdwcorp or ambevdw (both Iris available Azure Data warehouse) table.
    The arguments are:

    :param schema: name of the schema that will be written
    :type schema: String, required, not null

    :param table_name: name of the table that will be written
    :type table_name: String, required, not null

    :param mode: mode of spark write "append" or "overwrite"
    :type mode: String, required, not null

    :param temp_path: temporarily path in blob to intermediate load data in Azure Data Warehouse
    :type temp_path: String, required, not null

    :param options: another option accepted by Spark
    :type options: optional, dict
    """

    def __init__(
        self,
        schema: str,
        table_name: str,
        mode: str,
        temp_path: str,
        temp_container: str,
        options: Optional[dict] = None,
    ):
        self.table_name = table_name
        self.schema = schema
        self.mode = mode
        self.temp_path = temp_path
        self.temp_container = temp_container
        self.type = "dw_writer"
        self.options = options or None

    def get_table_name(self) -> str:
        """
        This method is responsible for returning the table name according to the Sql Data Warehouse format: schema.table.

        :return: the complete table name
        :rtype: string
        """
        return "{schema}.{table_name}".format(
            schema=self.schema, table_name=self.table_name
        )

    @staticmethod
    def get_url() -> str:
        """
        This method intends to return a string with the mounted url to write in DW (Azure Data Warehouse). This url
        is composed of "jdbc:sqlserver://{DW_SERVER_NAME};databaseName={DW_DATABASE_NAME};user={DW_USER};password={DW_PASSWORD}".
        The variables dwServerName, dwDatabaseName, dwUserName and dwPassword are obtained from Key Vault.

        :return: an url to direcionate to the dw
        :rtype: string
        """
        return "jdbc:sqlserver://{DW_SERVER_NAME};databaseName={DW_DATABASE_NAME};user={DW_USER};password={DW_PASSWORD}".format(
            DW_SERVER_NAME=get_key("dwServerName"),
            DW_DATABASE_NAME=get_key("dwDatabaseName"),
            DW_USER=get_key("dwUserName"),
            DW_PASSWORD=get_key("dwPassword"),
        )
