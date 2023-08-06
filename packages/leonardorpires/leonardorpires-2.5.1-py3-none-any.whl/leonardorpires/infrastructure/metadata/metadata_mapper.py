from typing import Dict, List

from pyiris.infrastructure.metadata.metadata import MetadataTable, MetadataTableSchema


class MetadataMapper(object):
    """
    A class responsible for mapping metadata file to metadata object.
    """

    @staticmethod
    def to_domain(metadata: Dict, repository: str) -> MetadataTable:
        """
        Map metadata file to metadata table.
        :param metadata: The valid metadata you want to create.
        :type metadata: dict

        :return: The result of metadata table object.
        :rtype: MetadataTable :class:`~pyiris.infrastructure.metadata.metadata.MetadataTable`

        """

        return MetadataTable(
            id=metadata.get("id"),
            repository=repository,
            name=metadata.get("name"),
            description=metadata.get("description"),
            team_owner=metadata.get("teamowner"),
            data_owner=metadata.get("dataowner"),
            data_expert=metadata.get("dataexpert"),
            data_lake_zone=metadata.get("datalakezone"),
            data_lake_path=metadata.get("datalakepath"),
            permission=metadata.get("permission"),
            country=metadata.get("country"),
            format=metadata.get("format"),
            partition_by_column=metadata.get("partitionbycolumn"),
            schema=MetadataMapper.to_schema_domain(metadata.get("schema")),
        )

    @staticmethod
    def to_schema_domain(schema: List[Dict]) -> List[MetadataTableSchema]:
        """
        Map metadata schema files to metadata schema tables.
        :param schema: The valid list of metadata schemas you want to create.
        :type schema: list(dict)

        :return: The results of metadata schema table object.
        :rtype: list(MetadataTable) :class:`~pyiris.infrastructure.metadata.metadata.MetadataTableSchema`
        """

        schema_domain = list()
        for column in schema:
            schema_domain.append(
                MetadataTableSchema(
                    id=column.get("id"),
                    metadata_table_id=column.get("metadata_table_id"),
                    name=column.get("name"),
                    type=column.get("type"),
                    description=column.get("description"),
                )
            )

        return schema_domain
