from pyiris.infrastructure.service.metadata.entity.dataset_metadata_entity import (
    DatasetSchema,
)


class DatasetSchemaMapper(object):
    """
    This class intends to map the metadata dict to a declarative base sqlalchemy object representing 'dataset_schema'
    table.
    """

    @staticmethod
    def to_table(metadata_schema):
        return DatasetSchema(
            name=metadata_schema.get("name"),
            type="string"
            if type(metadata_schema.get("type")) is dict
            else metadata_schema.get("type"),
            description=metadata_schema.get("description"),
        )
