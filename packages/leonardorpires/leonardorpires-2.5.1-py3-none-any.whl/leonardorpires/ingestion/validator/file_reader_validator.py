from typing import Dict, Union

from cerberus import Validator

from pyiris.infrastructure.common.either import Left, Right
from pyiris.ingestion.enums.enums import Countries, FileFormats
from pyiris.ingestion.validator.messages.custom_error_messages import (
    CustomCerberusErrorMessages,
)


class FileReaderValidator(object):
    """
    This class intends to validate the params to write files in write method. To validate we use Cerberus, a lib specializated in schema validate.
    The rules to approve the schemas are:

    table_id: required, not null, string, and have to be a snake_case;

    mount_name: required, not null, string

    country: required, not null, string and allowed only SAZ countries;

    path: required, not null, string

    format: required, not null, string and allowed only "parquet" and "avro;

    options: optional, not null and dict.

    """

    def __init__(self):
        self.validation_schema = {
            "table_id": {
                "required": True,
                "nullable": False,
                "type": "string",
                "regex": "[a-z0-9]+(_[a-z0-9]+)*",
            },
            "mount_name": {
                "required": True,
                "nullable": False,
                "type": "string",
            },
            "country": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": Countries,
            },
            "path": {
                "required": True,
                "nullable": False,
                "type": "string",
            },
            "format": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": FileFormats,
            },
            "options": {
                "required": False,
                "nullable": True,
                "type": "dict",
            },
        }
        self.filter_validator_schema = {"filter": {"type": "string", "nullable": False}}

    def consume_validate(self, file_reader: Dict) -> Union[Right, Left]:
        """
        The validate method is responsible for comparing the validation schema with the inputted schema
        composed of :class: pyiris.ingestion.extract.readers.file_reader.FileReader arguments.

        :param file_reader: the arguments of class :class:pyiris.ingestion.extract.readers.file_reader.FileReader
        :type file_reader: dict

        :return: a class with the validator result. If pyiris.infrastructure.common.either.Right(True), the inputted schema is accord to the validation schema. If pyiris.infrastructure.common.either.Left(validator.errors), the inputted schema does not match with validation schema.
        :rtype: Union[Right, Left]
        """
        validator = Validator(
            self.validation_schema,
            error_handler=CustomCerberusErrorMessages(class_to_validate="file_reader"),
            allow_unknown=True,
        )
        validator.validate(file_reader)

        if not validator.errors:
            return Right(True)
        else:
            return Left(validator.errors)

    def filter_validate(self, filter: dict) -> Union[Right, Left]:
        """
        The validate method is responsible for comparing the validation schema with the inputted schema
        composed of :class: pyiris.ingestion.extract.readers.file_reader.FileReader arguments._filter arguments.

        :param filter: the arguments of class pyiris.ingestion.extract.readers.file_reader.FileReader._filter
        :type filter: dict

        :return: a class with the validator result. If :class: pyiris.infrastructure.common.either.Right(True), the inputted schema is accord to the validation schema. If :class: pyiris.infrastructure.common.either.Left(validator.errors), the inputted schema does not match with validation schema.
        :rtype: Union[Right, Left]
        """
        validator = Validator(
            self.filter_validator_schema,
            error_handler=CustomCerberusErrorMessages(class_to_validate="file_reader"),
            allow_unknown=False,
        )
        validator.validate(filter)

        if not validator.errors:
            return Right(True)
        else:
            return Left(validator.errors)
