import pika
from pika.exceptions import AuthenticationError

from pyiris.infrastructure.common.exception import PyIrisConnectionException


class RabbitMQConnection(object):
    """
    This class intends to make a connection with RabbitMQ Broker.
    """

    @staticmethod
    def build(host, username, password, vhost=None):
        """
        This method is responsible for building a RabbitMQ connection and returning Blocking Connection object.

        :param host: a RabbitMQ host endpoint.
        :type host: String

        :param username: a RabbitMQ username for credentials.
        :type username: String

        :param password: a RabbitMQ password for credentials.
        :type password: String

        :param vhost: a RabbitMQ virtual host for provide logical grouping and separation of resources.
        :type vhost: String
        """

        try:
            credentials = pika.PlainCredentials(username=username, password=password)

            if vhost:
                return pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=host,
                        credentials=credentials,
                        virtual_host=vhost,
                        heartbeat=100,
                        blocked_connection_timeout=300,
                    )
                )
            else:
                return pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=host,
                        credentials=credentials,
                        heartbeat=100,
                        blocked_connection_timeout=300,
                    )
                )
        except AuthenticationError as e:
            raise PyIrisConnectionException(message=e)

        except Exception as e:
            raise PyIrisConnectionException(message=e)
