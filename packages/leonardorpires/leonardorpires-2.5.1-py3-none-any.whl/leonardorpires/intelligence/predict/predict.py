from abc import ABC, abstractmethod

from pyspark.sql import DataFrame


class Predict(ABC):
    @abstractmethod
    def load_model(self, *args):
        pass

    @abstractmethod
    def load_features(self) -> DataFrame:
        pass

    @abstractmethod
    def predict(self, *args, **kwargs) -> DataFrame:
        pass

    @abstractmethod
    def write_outputs(self, data: DataFrame) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
