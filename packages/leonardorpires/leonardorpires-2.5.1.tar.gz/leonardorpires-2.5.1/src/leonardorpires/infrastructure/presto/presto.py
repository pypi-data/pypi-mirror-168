from typing import Optional

from pyiris.infrastructure.presto.presto_connection import PrestoConnection


class Presto(object):
    """This class intends to interact with a Presto/Trino connection
    :class:pyiris.infrastructure.presto.presto_connection.PrestoConnection."""

    def __init__(self, connection=None):
        self.connection: Optional[PrestoConnection] = connection or PrestoConnection()

    def write(self, command: str) -> None:
        """This method intends to execute a command in a Presto/Trino through a connection.
        :param command: a command that will be executing
        :type command: string
        """
        with self.connection.cursor() as cursor:
            cursor.execute(command)
            cursor.fetchone()
