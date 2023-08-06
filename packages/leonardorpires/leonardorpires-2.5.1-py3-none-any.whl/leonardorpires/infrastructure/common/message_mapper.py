from typing import Dict, List

from pyiris.infrastructure.common.message import Message, MessageCategory


class MessageMapper(object):
    """
    A class responsible for mapping errors to a Message Object.
    """

    @staticmethod
    def to_validation_definition(key: Dict, error: List) -> Message:
        """
         Mapping to the validation category message.

        :param key: The key of message, e.g an column name.
        :type key: dict

        :param error: A list of errors that occur in the specific key.
        :type error: list

        :return: Returns the validation message for a specific key.
        :rtype: :class:`~pyiris.infrastructure.common.message.Message`
        """

        return Message(
            category=MessageCategory.VALIDATION.value,
            target=MessageMapper._to_camel_case(str(error[0])),
            key=key,
        )

    @staticmethod
    def to_validation_definitions(errors: Dict) -> List[Message]:
        """
        Mapping and returns a list of validation category message.

        :param errors: Errors that occur in the specific keys.
        :type errors: dict

        :return: List of returned :class:`~pyiris.infrastructure.common.message.Message` objects
        :rtype: list
        """

        return [
            MessageMapper.to_validation_definition(key, error)
            for key, error in errors.items()
        ]

    @staticmethod
    def _to_camel_case(snake_str: str):
        components = snake_str.split("_")
        return components[0] + "".join(
            component.title() for component in components[1:]
        )
