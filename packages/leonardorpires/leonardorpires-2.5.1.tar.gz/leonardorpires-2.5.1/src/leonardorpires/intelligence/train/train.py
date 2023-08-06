from abc import ABC, abstractmethod
from typing import Any


class Train(ABC):
    """
    This is the abstract class that will be extended for any training job to be ran and saved. It needs to have two abstract methods implemented,
    which are the train_definition and how to properly run it. If necessary, other methods might be implemented as well.
    """

    def __init__(self, model: Any = None):
        self.model = model

    @abstractmethod
    def train_definition(self, **kwargs) -> Any:
        """
        This method will define how the training should happen. Perhaps a simple

        ```python
        self.model.fit()
        ```

        Might already be enough, but often times it must be extended, and that is why keyword arguments are accepted as well.
        """
        pass

    @abstractmethod
    def run(self, **kwargs) -> None:
        """
        Defines how the job will be ran. Can take any input argument and should not return anything by default,
        but only call the train definition, along to whatever other methods necessary.
        """
        pass
