from typing import Optional

from pika import BlockingConnection

from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.enums.enums import WriterPriority
from pyiris.ingestion.load.writers.writer import Writer

logger = Logger(__name__)


class RabbitMQWriter(Writer):
    """
    This class intends to produce messages to a RabbitMQ Broker.
    :param engine: a RabbitMQ Blocking Connection object.
    :type engine: pika.BlockingConnection

    :param priority: the priority order to execute the writers
    :type priority: optional, integer
    """

    def __init__(self, engine: BlockingConnection, priority: Optional[int] = None):
        super().__init__(priority, engine)
        self.engine = engine
        self.priority = priority or WriterPriority.RABBITMQWRITER.value
        self.channel = self.engine.channel()

    def __exit__(self):
        self.channel.close()
        self.engine.close()

    @logger.log_decorator
    def write(self, **kwargs):
        """This method intends to handle how messages will be persisted to a specific exchange into RabbitMQ Broker.

        :param exchange_name: a RabbitMQ exchange name.
        :type exchange_name: String

        :param message: a message to be publish.
        :type message: bytes

        :param routing_key: a RabbitMQ message attribute that the exchange looks at when deciding how to route the message to queues.
        :type routing_key: String

        """
        self.channel.basic_publish(
            exchange=kwargs.get("exchange_name"),
            body=kwargs.get("message"),
            routing_key=kwargs.get("routing_key"),
        )
