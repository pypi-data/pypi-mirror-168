from typing import Dict, Union

from cerberus import Validator

from pyiris.infrastructure.common.either import Left, Right
from pyiris.ingestion.validator.messages.custom_error_messages import (
    CustomCerberusErrorMessages,
)


class JdbcReaderValidator(object):
    """
    This class intends to validate the params to write files in write method. To validate we use Cerberus, a lib
    specialized in schema validate.

    The rules to approve the schemas are:

    connection_string: required, not null, string

    user: required, not null, string

    password: required, not null, string

    table_name: required, not null, string, and have to be a snake_case

    options: not required, may be null, dict

    query: required, not null, string;
    """

    def __init__(self):
        self.validation_schema = {
            "connection_string": {
                "required": True,
                "nullable": False,
                "type": "string",
            },
            "table_id": {
                "required": True,
                "nullable": False,
                "type": "string",
            },
            "user": {
                "required": True,
                "nullable": False,
                "type": "string",
            },
            "password": {
                "required": True,
                "nullable": False,
                "type": "string",
            },
            "options": {
                "required": False,
                "nullable": True,
                "type": "dict",
            },
            "query": {"required": True, "nullable": False, "type": "string"},
        }

    def validate(self, jdbc_reader: Dict) -> Union[Right, Left]:
        """
        The validate method is responsible for comparing the validation schema with the inputted schema
        composed of :class: pyiris.ingestion.extract.readers.file_reader.FileReader arguments.

        :param jdbc_reader: the arguments of class :class:pyiris.ingestion.extract.readers.file_reader.FileReader
        :type jdbc_reader: dict

        :return: a class with the validator result. If pyiris.infrastructure.common.either.Right(True), the inputted schema is accord to the validation schema. If pyiris.infrastructure.common.either.Left(validator.errors), the inputted schema does not match with validation schema.
        :rtype: Union[Right, Left]
        """
        validator = Validator(
            self.validation_schema,
            error_handler=CustomCerberusErrorMessages(class_to_validate="jdbc_reader"),
            allow_unknown=True,
        )
        validator.validate(jdbc_reader)
        if not validator.errors:
            return Right(True)
        else:
            return Left(validator.errors)
