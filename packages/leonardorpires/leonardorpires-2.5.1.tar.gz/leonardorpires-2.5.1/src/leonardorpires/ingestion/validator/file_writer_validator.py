from typing import Dict, Union

from cerberus import Validator

from pyiris.infrastructure.common.either import Left, Right
from pyiris.ingestion.enums.enums import (
    Countries,
    ExternalMountNames,
    FileFormats,
    IrisMountNames,
    SyncModes,
)
from pyiris.ingestion.validator.messages.custom_error_messages import (
    CustomCerberusErrorMessages,
)


class FileWriterValidator(object):
    """
    This class intends to validate the params to write files in write method. To validate we use :class:cerberus.Validator,
    a lib specialized in schema validation.

    format: required, not null, string and allowed only "parquet" and "avro.

    path: required, not null, string, CamelCase with no special character (only numbers and letters) and required the follow hierarchy:

            - prelandingzone: System/Report
            - historyzone: System/Report
            - consumezone: Context/Domain/Report or more

    country: required, not null, string and allowed only SAZ countries.

    mount_name: required, not null, string and allowed only "consumezone", "prelandingzone", "historyzone",
    "privateconsumezone", "privateprelandingzone", "privatehistoryzone", "zxventures", "ztech", "brewdat" and "bifrost".

    mode: required, not null, string and allowed only "append" and "overwrite".

    partition_by: optional, not null, string and allowed only snake_case.
    """

    def __init__(self):
        self.validation_schema = {
            "format": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": FileFormats,
            },
            "path": {
                "required": True,
                "nullable": False,
                "type": "string",
                "regex": "(([A-Z0-9][a-z0-9]+)+/([A-Z0-9][a-z0-9]+)+)(/([A-Z0-9][a-z0-9]+)+)*",
            },
            "country": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": Countries,
            },
            "mount_name": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": list(ExternalMountNames._value2member_map_)
                + list(IrisMountNames._value2member_map_),
            },
            "mode": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": SyncModes,
            },
            "partition_by": {
                "required": False,
                "nullable": True,
                "anyof": [
                    {
                        "required": False,
                        "nullable": True,
                        "type": "string",
                        "regex": "[a-z0-9]+(_[a-z0-9]+)*",
                    },
                    {
                        "required": False,
                        "nullable": True,
                        "type": "list",
                        "minlength": 1,
                        "schema": {"type": "string", "regex": "[a-z0-9]+(_[a-z0-9]+)*"},
                    },
                ],
            },
        }

    def validate(self, file_writer: Dict) -> Union[Right, Left]:
        """
        The validate method is responsible for comparing the validation schema with the inputted schema composed of :class:pyiris.ingestion.load.writers.file_writer.FileWriter arguments.

        :param file_writer: the arguments of class :class:pyiris.ingestion.load.writers.file_writer.FileWriter
        :type file_writer: dict

        :return: a class with the validator result. If pyiris.infrastructure.common.either.Right(True), the inputted schema is matched with the validation schema. If pyiris.infrastructure.common.either.Left(validator.errors), the inputted schema does not match with validation schema.
        :rtype: Union[Right, Left]
        """
        validator = Validator(
            self.validation_schema,
            error_handler=CustomCerberusErrorMessages(class_to_validate="file_writer"),
            allow_unknown=True,
        )
        validator.validate(file_writer)

        if not validator.errors:
            return Right(True)
        else:
            return Left(validator.errors)
