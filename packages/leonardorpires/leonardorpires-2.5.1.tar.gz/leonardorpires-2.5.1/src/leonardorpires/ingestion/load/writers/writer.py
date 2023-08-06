from abc import ABC, abstractmethod
from typing import Union

from pika import BlockingConnection
from pyspark.sql import DataFrame

from pyiris.infrastructure import Presto, Spark
from pyiris.infrastructure.service.monitor.log.logger import Logger

logger = Logger(__name__)


class Writer(ABC):
    """
    This class intends to structure the writers subclasses.

    :param priority: the priority order to write
    :type priority: string

    :param engine: the writer executor
    :type engine: Union[Spark, Presto]
    """

    def __init__(self, priority: int, engine: Union[Spark, Presto, BlockingConnection]):
        self.priority = priority
        self.engine = engine

    @abstractmethod
    def write(self, dataframe: DataFrame):
        pass
