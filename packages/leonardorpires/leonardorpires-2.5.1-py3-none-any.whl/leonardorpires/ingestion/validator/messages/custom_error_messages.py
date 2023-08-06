import os
from abc import ABC
from typing import Any, Optional

import yaml
from cerberus import errors


class CustomMessages(object):
    def __init__(self, customized_messages: dict):
        self.customized_messages = customized_messages

    def get_message(self, field: str, class_to_validate: str, error_code: str):
        return self.customized_messages[field][error_code][class_to_validate]

    @staticmethod
    def build(file_path: str, category: str):
        with open(file_path) as messages:
            customized_messages = yaml.load(messages, Loader=yaml.FullLoader)[category]
        return CustomMessages(customized_messages=customized_messages)


class CustomCerberusErrorMessages(errors.BasicErrorHandler, ABC):
    def __init__(self, tree: Any = None, class_to_validate: Optional[str] = None):
        super().__init__(tree)
        self.class_to_validate = class_to_validate
        self.error_messages = CustomMessages.build(
            file_path=f"{os.path.dirname(__file__)}/custom_messages.yaml",
            category="cerberus",
        )

    def _format_message(self, field, error):
        if error.code in [65, 68, 36] and type(field) == str:
            self.messages[error.code] = self.error_messages.get_message(
                field=field,
                class_to_validate=self.class_to_validate,
                error_code=error.code,
            )
        return self.messages[error.code].format(
            *error.info, constraint=error.constraint, field=field, value=error.value
        )
