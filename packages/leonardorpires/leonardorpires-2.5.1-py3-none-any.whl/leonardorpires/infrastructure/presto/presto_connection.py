from contextlib import contextmanager

import trino
from trino.dbapi import Cursor
from trino.exceptions import TrinoExternalError, TrinoInternalError, TrinoUserError

from pyiris.infrastructure.common.config import get_key
from pyiris.infrastructure.common.exception import PyIrisConnectionException


class PrestoConnection(object):
    """This class intends to make a connection with Presto/Trino.

    :param connection: a created connection with presto based on environment variables "PRESTO_HOST", "PRESTO_PORT", "PRESTO_USER", "PRESTO_CATALOG".
    :type connection: trino.dbapi.connect
    """

    def __init__(self):
        self.connection = trino.dbapi.connect(
            host=get_key("PrestoHost"),
            port=get_key("PrestoPort"),
            user=get_key("PrestoUser"),
            catalog=get_key("PrestoCatalog"),
        )

    @contextmanager
    def cursor(self) -> Cursor:
        """This method intends to return a new :class:trino.dbapi.cursor based on a given :class:trino.dbapi.connect.

        Raises:
            TrinoUserError: [Presto user error.]
            TrinoExternalError: [Presto external error.]
            TrinoInternalError: [Presto internal error.]
            TrinoInternalError: [Error when trying to connect to Presto.]

        :return: a Trino cursor
        :rtype: trino.dbapi.cursor
        """
        cursor = self.connection.cursor()
        try:
            yield cursor
        except TrinoUserError as e:
            raise PyIrisConnectionException(message=e)

        except TrinoExternalError as e:
            raise PyIrisConnectionException(message=e)

        except TrinoInternalError as e:
            raise PyIrisConnectionException(message=e)

        except Exception as e:
            raise PyIrisConnectionException(message=e)
        finally:
            cursor.close()
