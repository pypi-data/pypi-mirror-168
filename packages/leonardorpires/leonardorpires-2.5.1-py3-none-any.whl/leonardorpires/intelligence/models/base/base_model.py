from abc import ABCMeta, abstractmethod

from mlflow.pyfunc import PythonModel


class BaseIrisModel(PythonModel, metaclass=ABCMeta):
    """
    This class will create a customized estimator object that will
    be responsible for train and predictions.

    It derives from the mlflow Pyfunc PythonModel base Class and needs
    some definitions to work properly, such as how to load the serialized model,
    how to fit the model, how you make predictions and so on.
    """

    @abstractmethod
    def load_context(self, context):
        pass

    @abstractmethod
    def load_training_data(self):
        pass

    @abstractmethod
    def fit(self, **kwargs):
        pass

    @abstractmethod
    def predict(self, context, data):
        pass

    @abstractmethod
    def get_signature(self, **kwargs):
        pass
