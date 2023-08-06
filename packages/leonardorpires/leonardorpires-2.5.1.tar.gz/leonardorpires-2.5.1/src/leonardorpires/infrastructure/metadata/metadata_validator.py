import re
from typing import Dict, Union

from cerberus import Validator

from pyiris.infrastructure.common.either import Left, Right
from pyiris.infrastructure.common.message_mapper import MessageMapper
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.enums.enums import (
    Countries,
    ExternalMountNames,
    FileFormats,
    IrisMountNames,
)

logger = Logger(__name__)


def find_whole_word(w):
    return re.compile(r"\b({0})\b".format(w), flags=re.IGNORECASE).search


def datalakepath_validation_rules(field, value, error):
    """
    Validate the given path against the following rules:
    - does not start with '/'
    - does not start with '/mnt/consumezone/'
    - does not have any of the following special characters:
    - dies not have any of the following keywords: 'teste', 'test', 'temp', 'backup', 'bkp', 'new', 'old', 'tmp', 'tempfiles'
    :param field: The field you want to validate.
    :type field: str
    :param value: The value of the field you want to validate.
    :type value: str
    :return: None
    """
    if value:
        if value.startswith("/"):
            error(str(field), 'Must not start with "/"')

        if value.startswith("/mnt/consumezone/"):
            error(str(field), 'Must not start with "/mnt/consumezone/"')

        special_characters = re.compile("[@!#$%^&*()<>?\\|}{~:]")
        if not (special_characters.search(value) is None):
            error(
                str(field),
                'Must not contain special characters "[@!#$%^&*()<>?\\|}{~:]"',
            )

        forbidden_words = [
            "teste",
            "test",
            "temp",
            "backup",
            "bkp",
            "new",
            "old",
            "tmp",
            "tempfiles",
        ]
        for forbidden_word in forbidden_words:
            if not (find_whole_word(forbidden_word)(value) is None):
                error(str(field), f'Must not contain the word: " {forbidden_word} "')


class MetadataValidator(object):
    """
    A class responsible for validating if the metadata is in accordance with rules.
    ...
    Attributes
    _validation_schema: dict
        The validation schema with the rules for each field.
    """

    def __init__(self):
        self._validation_schema = {
            "name": {"required": True, "nullable": False, "type": "string"},
            "description": {"required": True, "nullable": False, "type": "string"},
            "teamowner": {"required": True, "nullable": False, "type": "string"},
            "dataowner": {"required": True, "nullable": False, "type": "string"},
            "dataexpert": {"required": True, "nullable": False, "type": "string"},
            "datalakezone": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": list(ExternalMountNames._value2member_map_)
                + list(IrisMountNames._value2member_map_),
            },
            "datalakepath": {
                "required": True,
                "nullable": False,
                "type": "string",
                "check_with": datalakepath_validation_rules,
            },
            "permission": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": ["private", "public"],
            },
            "country": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": Countries,
            },
            "format": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": FileFormats,
            },
            "partitionbycolumn": {
                "required": False,
                "nullable": False,
                "type": "string",
            },
            "documentation_file_path": {
                "required": False,
                "nullable": False,
                "type": "string",
            },
            "classifications": {
                "required": False,
                "nullable": False,
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "type": {"required": True, "nullable": False, "type": "string"}
                    },
                },
            },
            "glossary": {
                "required": False,
                "nullable": False,
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "term": {"required": True, "nullable": False, "type": "string"}
                    },
                },
            },
            "schema": {
                "required": True,
                "nullable": False,
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "name": {"required": True, "nullable": False, "type": "string"},
                        "type": {"required": True, "nullable": False, "type": "string"},
                        "description": {
                            "required": True,
                            "nullable": False,
                            "type": "string",
                        },
                        "glossary": {
                            "required": False,
                            "nullable": False,
                            "schema": {
                                "type": "dict",
                                "schema": {
                                    "term": {
                                        "required": True,
                                        "nullable": False,
                                        "type": "string",
                                    }
                                },
                            },
                        },
                        "classifications": {
                            "required": False,
                            "nullable": False,
                            "type": "list",
                            "schema": {
                                "type": "dict",
                                "schema": {
                                    "type": {
                                        "required": True,
                                        "nullable": False,
                                        "type": "string",
                                    }
                                },
                            },
                        },
                    },
                },
            },
        }

    def validate(self, metadata: Dict) -> Union[Right, Left]:
        """
        Validate metadata against validation schema.
        :param metadata: The metadata you want to validate.
        :type metadata: dict
        :return: The results of validation.
        """
        validator = Validator(self._validation_schema, allow_unknown=False)
        validator.validate(metadata)
        if not validator.errors:
            return Right(metadata)
        else:
            errors = MessageMapper.to_validation_definitions(validator.errors)
            logger.error(
                'The validation process have failed for the "{metadata}" documentation. Check your documentation file at "{documentation_file_path}"'.format(
                    metadata=metadata.get("name"),
                    documentation_file_path=metadata.get("documentation_file_path"),
                )
            )
            for error in errors:
                logger.error(
                    "Key: {key} \n"
                    "Error: {error} \n"
                    "Category: {category}".format(
                        key=error.key, error=error.target, category=error.category
                    )
                )
            return Left(validator.errors)
