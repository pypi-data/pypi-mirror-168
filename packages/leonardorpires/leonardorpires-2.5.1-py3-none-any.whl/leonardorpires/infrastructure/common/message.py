from abc import ABC, abstractmethod
from enum import Enum


class MessageBuilder(ABC):
    def __init__(
        self,
        title: str,
        subtitle: str,
        image: str,
        message: str,
        color: str = None,
        link: str = None,
    ):
        self.title = title
        self.subtitle = subtitle
        self.image = image
        self.message = message
        self.color = color
        self.link = link

    @staticmethod
    @abstractmethod
    def build(task_name: str, message: str):
        pass


class ErrorMessage(MessageBuilder):
    def __init__(
        self,
        title: str,
        subtitle: str,
        image: str,
        message: str,
        traceback: str = None,
        color: str = None,
        link: str = None,
    ):
        super().__init__(title, subtitle, image, message, color, link)

        self.traceback = traceback

    @staticmethod
    def build(task_name: str, message: str, traceback: str = None):
        return ErrorMessage(
            title="Task Failed, please check!",
            subtitle="Failed to process a Task [**{task_name}**]".format(
                task_name=task_name.upper()
            ),
            image="https://i.imgur.com/M0BxtNZ.png",
            message=message,
            traceback=traceback,
            color="red",
            link=f"https://airflow-iris.ambev.com.br/dags/{task_name}/grid",
        )


class MessageCategory(Enum):
    """
    A class to represent an enumerate of error categories
    ¬
    """

    INFO = "INFO"
    VALIDATION = "VALIDATION"
    ERROR = "ERROR"


class Message(object):
    """
    A class to represent an error message.

    :param category: category of the message
    :type category: str

    :param target: target of the message
    :type target: str

    :param key: key of the message
    :type key: dict
    """

    def __init__(self, category=None, target=None, key=None):
        self.category = category
        self.target = target
        self.key = key

    def __eq__(self, other):
        return (
            self.category == other.category
            and self.target == other.target
            and self.key == other.key
        )
