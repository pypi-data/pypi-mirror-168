from typing import Union

from cerberus import Validator
from pyspark.sql.types import StructType

from pyiris.infrastructure.common.either import Left, Right
from pyiris.ingestion.enums.enums import ExternalMountNames, IrisMountNames


class MetadataTableValidator(object):
    def __init__(self):
        self._validation_schema = {
            "name": {"required": True, "nullable": False, "type": "string"},
            "description": {"required": True, "nullable": False, "type": "string"},
            "owner": {"required": True, "nullable": False, "type": "string"},
            "domain": {"required": False, "nullable": True, "type": "string"},
            "data_lake_zone": {
                "required": True,
                "nullable": False,
                "type": "string",
                "allowed": list(ExternalMountNames._value2member_map_)
                + list(IrisMountNames._value2member_map_),
            },
            "data_lake_path": {"required": True, "type": "string"},
            "partition_by_column": {"required": False, "type": "string"},
            "personal_data": {"required": True, "type": "boolean"},
        }

    def validate(self, metadata) -> Union[Right, Left]:
        validator = Validator(self._validation_schema, allow_unknown=False)
        validator.validate(metadata.__dict__)
        if not validator.errors:
            return Right(None)
        else:
            return Left(validator.errors)


class MetadataTableColumnValidator:
    def __init__(self):
        self._validation_schema = {
            "name": {"required": True, "nullable": False, "type": "string"},
            "column_type": {"required": True, "nullable": False, "type": "string"},
            "description": {"required": True, "nullable": False, "type": "string"},
        }

    def validate(self, schema: StructType) -> Union[Right, Left]:
        metadata_table_column_dicts = MetadataTableColumnValidator.to_dicts(schema)
        validator = Validator(self._validation_schema, allow_unknown=False)

        for column_dict in metadata_table_column_dicts:
            validator.validate(column_dict)
            if not validator.errors:
                return Right(True)
            else:
                return Left(validator.errors)

    @staticmethod
    def to_dict(column):
        return {
            "name": str(column.name),
            "column_type": str(column.dataType),
            "description": column.metadata["description"],
        }

    @staticmethod
    def to_dicts(schema):
        return list(map(MetadataTableColumnValidator.to_dict, schema.fields))
