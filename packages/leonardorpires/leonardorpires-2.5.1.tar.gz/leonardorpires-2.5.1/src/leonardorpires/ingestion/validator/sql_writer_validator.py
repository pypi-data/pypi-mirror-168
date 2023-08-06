from typing import Dict, Union

from cerberus import Validator

from pyiris.infrastructure.common.either import Left, Right
from pyiris.ingestion.enums.enums import SyncModes
from pyiris.ingestion.validator.messages.custom_error_messages import (
    CustomCerberusErrorMessages,
)


class SqlWriterValidator(object):
    """
    This class intends to validate the params to write a table in write :class:pyiris.ingestion.load.writers.dw_writer.DwWriter. We use :class:cerberus.Validator,
    a lib specialized in schema validation to perform this.

    table_name: required, not null, string and snake_case

    schema: required, not null, string and snake_case

    mode: required, not null, string and allowed only "append" and "overwrite"

    temp_path: required, not null, string and accord to regex
    '(([A-Z0-9][a-z0-9]+)+/([A-Z0-9][a-z0-9]+)+)(/([A-Z0-9][a-z0-9]+)+)*'
    """

    def __init__(self):
        self.validation_schema = {
            "table_name": {
                "required": True,
                "nullable": False,
                "type": "string",
                "regex": "[a-z0-9]+(_[a-z0-9]+)*",
            },
            "schema": {
                "required": True,
                "nullable": False,
                "type": "string",
                "regex": "[a-z0-9]+(_[a-z0-9]+)*",
            },
            "mode": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": SyncModes,
            },
            "temp_path": {
                "required": False,
                "nullable": False,
                "type": "string",
                "regex": "(([A-Z0-9][a-z0-9]+)+/([A-Z0-9][a-z0-9]+)+)(/([A-Z0-9][a-z0-9]+)+)*",
            },
        }

    def validate(self, sql_params: Dict) -> Union[Right, Left]:
        """
        The validate method is responsible for comparing the validation schema with the inputted schema composed of :class:pyiris.ingestion.load.writers.sql_writer.SqlWriter arguments.

        :param sql_params: the arguments of class :class:pyiris.ingestion.load.writers.sql_writer.SqlWriter
        :type sql_params: dict

        :return: a class with the validator result. If pyiris.infrastructure.common.either.Right(True), the inputted schema is matched with the validation schema. If pyiris.infrastructure.common.either.Left(validator.errors), the inputted schema does not match with validation schema.
        :rtype: Union[Right, Left]
        """
        validator = Validator(
            self.validation_schema,
            error_handler=CustomCerberusErrorMessages(class_to_validate="sql_writer"),
            allow_unknown=True,
        )
        validator.validate(sql_params)

        if not validator.errors:
            return Right(True)
        else:
            return Left(validator.errors)
