from typing import Dict, Union

from cerberus import Validator

from pyiris.infrastructure.common.either import Left, Right
from pyiris.ingestion.enums.enums import (
    Countries,
    ExternalMountNames,
    IrisMountNames,
    PrestoFormat,
)
from pyiris.ingestion.validator.messages.custom_error_messages import (
    CustomCerberusErrorMessages,
)


class PrestoWriterValidator(object):
    """
    This class intends to validate the params to write files in write method. To validate we use :class:cerberus.Validator,
    a lib specialized in schema validation.
    format: required, not null, string and allowed only "parquet".
    path: required, not null, string, CamelCase with no special character (only numbers and letters) and required the follow hierarchy:
            - prelandingzone: System/Report
            - historyzone: System/Report
            - consumezone: Context/Domain/Report or more
    country: required, not null, string and allowed only SAZ countries.
    mount_name: required, not null, string and allowed only "consumezone", "prelandingzone", "historyzone",
    "privateconsumezone", "privateprelandingzone", "privatehistoryzone" and "bifrost.
    schema: required, not null, string and snake_case
    table_name: required, not null, string and snake_case
    partition_by: optional, not null, string and allowed only snake_case.
    sync_mode: optional, string, allowed only FULL, ADD and DROP.
    """

    def __init__(self):
        self.validation_schema = {
            "format": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": PrestoFormat,
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
            "schema": {
                "required": True,
                "nullable": False,
                "type": "string",
                "regex": "[a-z0-9]+(_[a-z0-9]+)*",
            },
            "table_name": {
                "required": True,
                "nullable": False,
                "type": "string",
                "regex": "[a-z0-9]+(_[a-z0-9]+)*",
            },
            "sync_mode": {
                "required": False,
                "nullable": True,
                "type": "string",
                "allowed": ["ADD", "FULL", "DROP"],
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

    def validate(self, presto_writer: Dict) -> Union[Right, Left]:
        """
        The validate method is responsible for comparing the validation schema with the inputted schema composed of :class:pyiris.ingestion.load.writers.presto_writer.PrestoWriter arguments.
        :param presto_writer: the arguments of class :class:pyiris.ingestion.load.writers.presto_writer.PrestoWriter
        :type presto_writer: dict
        :return: a class with the validator result. If pyiris.infrastructure.common.either.Right(True), the inputted schema is matched with the validation schema. If pyiris.infrastructure.common.either.Left(validator.errors), the inputted schema does not match with validation schema.
        :rtype: Union[Right, Left]
        """
        validator = Validator(
            self.validation_schema,
            error_handler=CustomCerberusErrorMessages(
                class_to_validate="presto_writer"
            ),
            allow_unknown=True,
        )
        validator.validate(presto_writer)

        if not validator.errors:
            return Right(True)
        else:
            return Left(validator.errors)
