from typing import List
from uuid import uuid4


class MetadataTableSchema(object):
    """
    A class to represent metadata table schema.

    :param id: The identifier of the metadata table schema.
    :type id: str

    :param metadata_table_id: The identifier of the metadata table.
    :type metadata_table_id: str

    :param name: The column name in the table schema.
    :type name: str

    :param type: The column type in the table schema.
    :type type: str

    :param description: The description in the table schema.
    :type description: str

    """

    def __init__(
        self,
        id: str,
        metadata_table_id: str,
        name: str,
        type: str,
        description: str,
    ):
        self.id = id or uuid4()
        self.metadata_table_id = metadata_table_id
        self.name = name
        self.type = type
        self.description = description

    def __eq__(self, other):
        return other and self.__dict__ == other.__dict__


class MetadataTable(object):
    """
    A class to represent metadata table.

    :param id: The identifier of the metadata table.
    :type id: str

    :param name: The name of metadata table.
    :type name: str

    :param description: The description of metadata table.
    :type description: str

    :param team_owner: The team_owner of metadata table.
    :type team_owner: str

    :param data_owner: The data_owner of metadata table.
    :type data_owner: str

    :param data_expert: The data_expert of metadata table.
    :type data_expert: str

    :param data_owner: The data_owner of metadata table.
    :type data_owner: str

    :param data_lake_zone: The data_lake_zone of metadata table.
    :type data_lake_zone: str

    :param data_lake_path: The data_lake_path of metadata table.
    :type data_lake_path: str

    :param permission: The permission of metadata table.
    :type permission: str

    :param country: The country of metadata table.
    :type country: str

    :param format: The format of metadata table.
    :type format: str

    :param partition_by_column: The partition column of metadata table.
    :type partition_by_column: str

    :param schema: The schema of metadata table.
    :type schema: list(MetadataTableSchema): :class:`~pyiris.infrastructure.metadata.metadata.api.MetadataTableSchema`
    """

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        team_owner: str,
        data_owner: str,
        data_expert: str,
        data_lake_zone: str,
        data_lake_path: str,
        permission: str,
        country: str,
        format: str,
        partition_by_column: str,
        repository: str,
        schema: List[MetadataTableSchema] = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.description = description
        self.team_owner = team_owner
        self.data_owner = data_owner
        self.data_expert = data_expert
        self.data_lake_zone = data_lake_zone
        self.data_lake_path = data_lake_path
        self.permission = permission
        self.country = country
        self.format = format
        self.partition_by_column = partition_by_column
        self.repository = repository
        self.schema = schema

    def __eq__(self, other):
        return other and self.__dict__ == other.__dict__
