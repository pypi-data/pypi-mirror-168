from azure.servicebus import ServiceBusClient
from azure.servicebus.exceptions import (
    ServiceBusAuthenticationError,
    ServiceBusAuthorizationError,
)

from pyiris.infrastructure.common.exception import PyIrisConnectionException


class ServiceBusConnection(object):
    """
    This class intends to make a connection with ServiceBus Broker.
    """

    @staticmethod
    def build(connection_string: str):
        """
        This method is responsible for building a ServiceBus connection and returning Blocking Connection object.

        :param connection_string: a ServiceBus connection string url.
        :type connection_string: String
        """
        try:
            return ServiceBusClient.from_connection_string(conn_str=connection_string)
        except ServiceBusAuthenticationError as e:
            raise PyIrisConnectionException(message=e)
        except ServiceBusAuthorizationError as e:
            raise PyIrisConnectionException(message=e)
        except Exception as e:
            raise PyIrisConnectionException(message=e)
