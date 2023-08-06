from abc import ABCMeta
from typing import Any, Dict, List, Optional

import mlflow

from pyiris.intelligence.train.train import Train


class PyfuncTrain(Train, metaclass=ABCMeta):
    """
    This class is implemented to work as a guideline for training a model as a PyFunc. It will ask the user to
    inform a model object, as well as parameters, metrics and code to log along with the training module.
    This will guarantee more governance and visibility throughout the overall development process.

    :param model: The model object to be trained. The train definition will basically call this object to fit.
    :type model: Any

    :param metrics_dict: A key-value pair of desired metrics to log along with the trained model
    :type metrics_dict: dict

    :param params_dict: A key-value pair of parameters (usually, but not exclusively, hyperparameters)
    to log with the trained model
    :type params_dict: dict

    :param conda_env: Can either be a string with the path to the conda environment or a dictionary with the
     proper conda environment definition
    :type conda_env: Either a dictionary or string

    :param code: The code to be logged along with the model. If the user, for example, defines another object outside
    their train.py and need that module for reference when predicting. It is optional and defaults to None.
    :type code: List[str]
    """

    def __init__(
        self,
        model: Any = None,
        metrics_dict: Dict = None,
        params_dict: Dict = None,
        conda_env: Any = None,
        code: Optional[List[str]] = None,
    ):
        super().__init__(model=model)
        self.conda_env = conda_env
        self.code = code
        self.metrics_dict = metrics_dict
        self.params_dict = params_dict

    def train_definition(self, **kwargs) -> None:
        """
        Since this class should always be extended, this method can also take any number of keyword arguments as input.
        The user should properly define how to fit their model. Perhaps a simple

        ```python
        self.model.fit()
        ```

        Might already be enough, but often times it must be extended.
        Since the goal is to simply state which are the calls to be made, it won't have any returns, but only call what is necessary
        to fit the model.
        """
        pass

    def log_model(self) -> None:
        """
        This method will log the model using mlflow's pyfunc method. It makes sure the user is inputting a code_path, a conda environment dict or
        file path and the Python Model used for training.
        """
        mlflow.pyfunc.log_model(
            python_model=self.model,
            artifact_path="model",
            conda_env=self.conda_env,
            code_path=self.code,
        )

    def log_params(self) -> None:
        """
        This method will check if a training parameters dictionary was declared on the constructor and call the mlflow log_params method.
        Otherwise, it will raise a ValueError indicating that the user must log their parameteres for training.
        """
        if self.params_dict:
            mlflow.log_params(self.params_dict)
        else:
            raise ValueError(
                "You must specify a params_dict in your constructor  to log your PyFunc model!"
            )

    def log_metrics(self) -> None:
        """
        This method will check if a metrics dictionary was declared on the constructor and call the mlflow log_metrics method.
        Otherwise, it will raise a ValueError indicating that the user must log their metrics for training.
        """
        if self.metrics_dict:
            mlflow.log_metrics(self.metrics_dict)
        else:
            raise ValueError(
                "You must specify the metrics_dict in your constructor to log your Pyfunc model!"
            )

    def run(self) -> None:
        """ "
        This method will chain together the train definition, logging the model, train parameters and metrics.
        It was designed to make sure that every PyFunc will have at least one dictionary of parameters, metrics and
        correctly have their model logged along with the code.
        """
        self.train_definition()
        self.log_model()
        self.log_params()
        self.log_metrics()
