from abc import ABC, abstractmethod

from pyspark.sql import DataFrame

from pyiris.infrastructure.service.monitor.log.logger import Logger

logger = Logger(__name__)


class Transformation(ABC):
    """This class intends to structure the transformation subclasses.

    :param name: the name of the transformation
    :type name: string

    :param description: the description of the transformation
    :type engine: string
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @logger.log_decorator
    @abstractmethod
    def transform(self, dataframe: DataFrame) -> DataFrame:
        pass
