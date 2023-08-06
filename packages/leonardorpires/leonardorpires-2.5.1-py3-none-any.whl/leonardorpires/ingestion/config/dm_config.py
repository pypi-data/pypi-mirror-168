from typing import Optional

from pyiris.infrastructure.common.config import get_key


class DmWriterConfig(object):
    """
    This class intends to get configs to write a Iris data mart (Microsoft Sql Server) table, especially for the people
    analytics Sql Server. The arguments are:

    :param schema: name of the schema that will be written
    :type schema: String, required, not null

    :param table_name: name of the table that will be written
    :type table_name: String, required, not null

    :param mode: mode of spark write "append" or "overwrite"
    :type mode: String, required, not null

    :param truncate: define is the existent table will be truncated
    :type truncate: String, optional, not null, default = True

    :param options: another option accepted by spark
    :type options: optional, dict
    """

    def __init__(
        self,
        schema: str,
        table_name: str,
        mode: str,
        truncate: str,
        options: Optional[dict] = None,
    ):
        self.table_name = table_name
        self.schema = schema
        self.mode = mode
        self.truncate = truncate
        self.options = options or None
        self.type = "jdbc"

    def get_table_name(self) -> str:
        """
        This method is responsible for returning the table name according to the Sql Server format: schema.table.

        :return: the complete table name
        :rtype: string
        """
        return "{schema}.{table_name}".format(
            schema=self.schema, table_name=self.table_name
        )

    @staticmethod
    def get_url() -> str:
        """
        This method intends to return a str with the mounted url to write in the Microsoft SQL Server. This url is
        composed of "jdbc:sqlserver://{DM_SERVER_NAME}:{DM_SERVER_PORT};database={DM_DATABASE_NAME};user={
        DM_USER};password={DM_PASSWORD}".
        The variables dmServerName, dmServerPort, dmDatabaseName, dmUserName and dmPassword are obtained from Key
        Vault.

        :return: an url to direcionate to the DM
        :rtype: str
        """
        return "jdbc:sqlserver://{DM_SERVER_NAME}:{DM_SERVER_PORT};database={DM_DATABASE_NAME};user={DM_USER};password={DM_PASSWORD}".format(
            DM_SERVER_NAME=get_key("dmServerName"),
            DM_SERVER_PORT=get_key("dmServerPort"),
            DM_DATABASE_NAME=get_key("dmDatabaseName"),
            DM_USER=get_key("dmUserName"),
            DM_PASSWORD=get_key("dmPassword"),
        )
