import random
from typing import Dict, List
from uuid import uuid4

from pyiris.infrastructure.common.config import get_key
from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.ingestion.task.entity.task_entity import TaskEntity


def generate_guid() -> str:
    return str(random.randint(10, 10000000000) * -1)


class PurviewMapper(object):
    """
    A class responsible for mapping metadata file to Purview API requests.
    """

    @staticmethod
    def get_adls_name(permission: str) -> str:
        if permission == "public":
            return get_key("IrisAdlsName")
        elif permission == "private":
            return get_key("IrisAdlsNamePrivate")

    @staticmethod
    def to_azure_resource_set_request_by_object(
        task_entity: TaskEntity,
        metadata_entity: MetadataEntity,
        glossary_terms: List[Dict],
    ) -> Dict:
        """
        Create purview resource set entities request.
        :param task_entity: The respective task entity object
        :type task_entity: TaskEntity

        :param metadata_entity: The respective metadata entity object
        :type metadata_entity: MetadataEntity

        :param glossary_terms: The list of all glossary terms store into Purview Backend Catalog. Supports a list of dicts.
        :type glossary_terms: list(dict)

        :return: The results of your bulk entity create.
        :rtype: dict
        """

        entities = list()
        referred_entities = dict()
        metadata_dict = dict()
        metadata_dict["datalakepath"] = task_entity.path
        metadata_dict["datalakezone"] = "trustedzone"
        metadata_dict["name"] = task_entity.name
        metadata_dict["description"] = metadata_entity.description
        metadata_dict["dataowner"] = task_entity.task_owner
        metadata_dict["dataexpert"] = metadata_entity.dataexpert
        metadata_dict["country"] = task_entity.country
        metadata_dict["format"] = task_entity.format
        metadata_dict["teamowner"] = task_entity.owner_team
        metadata_dict["permission"] = task_entity.permission or "public"
        metadata_dict["partitionbycolumn"] = task_entity.partition_by
        metadata_dict["classifications"] = metadata_entity.classifications
        metadata_dict["glossary"] = metadata_entity.glossary
        metadata_dict["schema"] = metadata_entity.schema
        resource_set_guid = generate_guid()
        tabular_schema_guid = generate_guid()
        path_entities = AzureDataLakeGen2PathMapper.to_entities(metadata=metadata_dict)
        column_entities = ColumnsMapper.to_entities(
            metadata=metadata_dict, glossary_terms=glossary_terms
        )

        resource_set_entity = AzureDataLakeGen2FileMapper.to_entity(
            metadata=metadata_dict,
            columns=column_entities,
            resource_set_guid=resource_set_guid,
            tabular_schema_guid=tabular_schema_guid,
            glossary_terms=glossary_terms,
        )

        tabular_schema_entity = TabularSchemaMapper.to_entity(
            tabular_schema_guid=tabular_schema_guid,
            resource_set_guid=resource_set_guid,
            columns=column_entities,
            datalake_path=metadata_dict.get("datalakepath"),
        )

        referred_entities.update(tabular_schema_entity)
        [referred_entities.update(column_entity) for column_entity in column_entities]

        entities.extend(path_entities)
        entities.append(resource_set_entity)
        return {"entities": entities, "referredEntities": referred_entities}

    @staticmethod
    def to_azure_resource_set_request(
        metadata: List[Dict], glossary_terms: List[Dict]
    ) -> Dict:
        """
        Create purview resource set entities request.
        :param metadata: The list of valid metadata you want to create. Supports a list of dicts.
        :type metadata: list(dict)

        :param glossary_terms: The list of all glossary terms store into Purview Backend Catalog. Supports a list of dicts.
        :type glossary_terms: list(dict)

        :return: The results of your bulk entity create.
        :rtype: dict
        """

        entities = list()
        referred_entities = dict()
        for metadata in metadata:
            metadata.get("datalakepath")
            metadata.get("datalakezone")
            metadata.get("name")
            metadata.get("dataowner")
            metadata.get("teamowner")
            metadata.get("partitionbycolumn")
            resource_set_guid = generate_guid()
            tabular_schema_guid = generate_guid()
            path_entities = AzureDataLakeGen2PathMapper.to_entities(metadata=metadata)
            column_entities = ColumnsMapper.to_entities(
                metadata=metadata, glossary_terms=glossary_terms
            )

            resource_set_entity = AzureDataLakeGen2FileMapper.to_entity(
                metadata=metadata,
                columns=column_entities,
                resource_set_guid=resource_set_guid,
                tabular_schema_guid=tabular_schema_guid,
                glossary_terms=glossary_terms,
            )

            tabular_schema_entity = TabularSchemaMapper.to_entity(
                tabular_schema_guid=tabular_schema_guid,
                resource_set_guid=resource_set_guid,
                columns=column_entities,
                datalake_path=metadata.get("datalakepath"),
            )

            referred_entities.update(tabular_schema_entity)
            [
                referred_entities.update(column_entity)
                for column_entity in column_entities
            ]

            entities.extend(path_entities)
            entities.append(resource_set_entity)

        return {"entities": entities, "referredEntities": referred_entities}


class AzureDataLakeGen2FileMapper(object):
    """
    A class responsible for mapping to Azure Data Lake Gen2 Resource Set Entity.
    """

    @staticmethod
    def to_entity(
        metadata: Dict,
        columns: List[Dict],
        resource_set_guid: uuid4,
        tabular_schema_guid: uuid4,
        glossary_terms: List[Dict],
    ) -> Dict:
        """
        Map metadata to azure resource set entities.
        :param metadata: The valid metadata you want to create.
        :type metadata: dict

        :param columns: The list of columns for the metadata.
        :type columns: list(dict)

        :param resource_set_guid: The resource set guid identifier.
        :type resource_set_guid: str

        :param tabular_schema_guid: The tabular schema guid identifier.
        :type tabular_schema_guid: str

        :param glossary_terms: The list of all glossary terms store into Purview Backend Catalog. Supports a list of dicts.
        :type glossary_terms: list(dict)

        :return: The results of azure data lake resource set mapping.
        :rtype: dict
        """

        return {
            "guid": resource_set_guid,
            "typeName": "azure_datalake_gen2_path",
            "attributes": {
                "name": metadata.get("name"),
                "description": metadata.get("description"),
                "path": metadata.get("datalakepath"),
                "isFile": True,
                "owner": metadata.get("dataowner"),
                "qualifiedName": "https://{adls_name}.dfs.core.windows.net/{datalakezone}/{datalakepath}/{name}".format(
                    adls_name=PurviewMapper.get_adls_name(
                        permission=metadata.get("permission")
                    ),
                    datalakezone=metadata.get("datalakezone"),
                    datalakepath=metadata.get("datalakepath"),
                    name=metadata.get("name"),
                ),
                "userProperties": {
                    "teamOwner": metadata.get("teamowner"),
                    "dataOwner": metadata.get("dataowner"),
                    "dataExpert": metadata.get("dataexpert"),
                    "dataLakeZone": metadata.get("datalakezone"),
                    "dataLakePath": metadata.get("datalakepath"),
                    "permission": metadata.get("permission"),
                    "country": metadata.get("country"),
                    "format": metadata.get("format"),
                    "partitionByColumn": metadata.get("partitionbycolumn")
                    if metadata.get("partitionbycolumn")
                    else None,
                },
            },
            "columns": ColumnsMapper.build_referred_entity_columns(columns=columns)
            if columns
            else [],
            "relationshipAttributes": {
                "inputToProcesses": [],
                "schema": [],
                "attachedSchema": [],
                "meanings": GlossaryMapper.to_entity(
                    glossary_terms=glossary_terms,
                    metadata_glossary_terms=metadata.get("glossary")
                    if metadata.get("glossary")
                    else [],
                ),
                "outputFromProcesses": [],
                "tabular_schema": {
                    "guid": tabular_schema_guid,
                    "typeName": "tabular_schema",
                    "entityStatus": "ACTIVE",
                    "displayText": "{dataset_name} Tabular Schema".format(
                        dataset_name=metadata.get("name")
                    ),
                    "relationshipType": "tabular_schema_datasets",
                    "relationshipStatus": "ACTIVE",
                    "relationshipAttributes": {"typeName": "tabular_schema_datasets"},
                },
            },
            "classifications": list(
                map(ClassificationsMapper.to_entity, metadata.get("classifications"))
            )
            if metadata.get("classifications")
            else [],
        }


class AzureDataLakeGen2PathMapper(object):
    """
    A class responsible for mapping to Azure Data Lake Gen2 Path Entity.
    """

    @staticmethod
    def to_entities(metadata: Dict) -> List[Dict]:
        """
        Map metadata to azure data lake gen2 path entities.
        :param metadata: The valid metadata you want to mapping to azure data lake path entity.
        :type metadata: dict

        :return: The results of azure data lake path entities mapping.
        :rtype: dict
        """

        qualified_name = str()
        path_entities = list()
        folders = metadata.get("datalakepath").split("/")
        for folder in folders:
            qualified_name += "/{folder}".format(folder=folder)
            path_entities.append(
                {
                    "guid": "-{folder}".format(folder=folder),
                    "typeName": "azure_datalake_gen2_path",
                    "status": "ACTIVE",
                    "displayText": folder,
                    "attributes": {
                        "isFile": False,
                        "qualifiedName": "https://{adls_name}.dfs.core.windows.net/{datalakezone}{qualified_name}/".format(
                            adls_name=PurviewMapper.get_adls_name(
                                permission=metadata.get("permission")
                            ),
                            datalakezone=metadata.get("datalakezone"),
                            qualified_name=qualified_name,
                        ),
                        "name": folder,
                    },
                }
            )

        return path_entities


class TabularSchemaMapper(object):
    """
    A class responsible for mapping to Tabular Schema Entity.
    """

    @staticmethod
    def to_entity(
        tabular_schema_guid: str,
        resource_set_guid: str,
        columns: List[Dict],
        datalake_path: str,
    ) -> Dict:
        """
        Map to tabular schema entity.
        :param tabular_schema_guid: The tabular schema guid identifier.
        :type tabular_schema_guid: str

        :param resource_set_guid: The resource set guid identifier.
        :type resource_set_guid: str

        :param columns: The list of columns for the metadata..
        :type columns: list(dict)

        :param datalake_path: The datalake path to build a qualified name.
        :type datalake_path: dict

        :return: The result of tabular schema entity.
        :rtype: dict
        """

        return {
            tabular_schema_guid: {
                "typeName": "tabular_schema",
                "attributes": {
                    "qualifiedName": "{datalake_path}#__tabular_schema/{guid}".format(
                        datalake_path=datalake_path, guid=tabular_schema_guid
                    ),
                    "name": "tabular_schema",
                    "format": None,
                    "description": None,
                },
                "guid": tabular_schema_guid,
                "relationshipAttributes": {
                    "inputToProcesses": [],
                    "schema": [],
                    "associatedDataSets": [
                        {
                            "guid": resource_set_guid,
                            "typeName": "azure_datalake_gen2_resource_set",
                            "entityStatus": "ACTIVE",
                            "displayText": "Azure DataLake Gen2 Resource Set",
                            "relationshipType": "tabular_schema_datasets",
                            "relationshipStatus": "ACTIVE",
                            "relationshipAttributes": {
                                "typeName": "tabular_schema_datasets"
                            },
                        }
                    ],
                    "columns": ColumnsMapper.build_referred_entity_columns(columns)
                    if columns
                    else [],
                },
            }
        }


class ColumnsMapper(object):
    """
    A class responsible for mapping to Column Entity.
    """

    @staticmethod
    def to_entity(column: Dict, glossary_terms: List[Dict]) -> Dict:
        """
        Map to column entity.
        :param column: The column of metadata.
        :type column: dict

        :param glossary_terms: The list of all glossary terms store into Purview Backend Catalog. Supports a list of dicts.
        :type glossary_terms: list(dict)

        :return: The result of column entity mapping.
        :rtype: dict
        """
        guid = generate_guid()

        return {
            guid: {
                "guid": guid,
                "typeName": "column",
                "entityStatus": "ACTIVE",
                "attributes": {
                    "qualifiedName": "{column_name}#_column/{guid}".format(
                        column_name=column.get("name"), guid=guid
                    ),
                    "name": column.get("name"),
                    "type": column.get("type"),
                    "description": column.get("description"),
                },
                "relationshipAttributes": {
                    "meanings": GlossaryMapper.to_entity(
                        glossary_terms=glossary_terms,
                        metadata_glossary_terms=column.get("glossary")
                        if column.get("glossary")
                        else [],
                    ),
                },
                "classifications": list(
                    map(ClassificationsMapper.to_entity, column.get("classifications"))
                )
                if column.get("classifications")
                else [],
            }
        }

    @staticmethod
    def to_entities(metadata: Dict, glossary_terms: List[Dict]) -> List[Dict]:
        """
        Map to column entities.
        :param metadata: The list of valid metadata.
        :type metadata: dict

        :param glossary_terms: The list of all glossary terms store into Purview Backend Catalog. Supports a list of dicts.
        :type glossary_terms: list(dict)

        :return: The result of column entities mapping.
        :rtype: list(dict)
        """

        return [
            ColumnsMapper.to_entity(column, glossary_terms)
            for column in metadata.get("schema")
        ]

    @staticmethod
    def build_referred_entity_columns(columns: List[Dict]) -> List[Dict]:
        """
        Map metadata columns to purview columns entity.
        :param columns: The valid metadata you want to create.
        :type columns: list(dict)

        :return: The results of resource set columns.
        :rtype: list(dict)
        """

        resource_set_columns = list()
        for column in columns:
            for key, value in column.items():
                resource_set_columns.append(
                    {"guid": value.get("guid"), "typeName": value.get("typeName")}
                )

        return resource_set_columns


class ClassificationsMapper(object):
    """
    A class responsible for mapping to Classification Entity.
    """

    @staticmethod
    def to_entity(classification: Dict) -> Dict:
        """
        Map to column entities.
        :param classification: The metadata classification.
        :type classification: dict

        :return: The result if metadata classification mapping.
        :rtype: dict
        """
        return {"typeName": classification.get("type")}


class GlossaryMapper(object):
    """
    A class responsible for mapping to Glossary Entity.
    """

    @staticmethod
    def to_entity(
        glossary_terms: List[Dict], metadata_glossary_terms: List[Dict]
    ) -> List[Dict]:
        """
        Map to glossary term entities.
        :param glossary_terms: The list of all glossary terms store into Purview Backend Catalog. Supports a list of dicts.
        :type glossary_terms: list(dict)

        :param metadata_glossary_terms: The list of all glossary terms into metadata dataset file. Supports a list of dicts.
        :type metadata_glossary_terms: list(dict)

        :return: Glossary terms entities.
        :rtype: dict
        """

        terms = list()
        for metadata_glossary_term in metadata_glossary_terms:
            for glossary_term in glossary_terms:
                if glossary_term.get("status") == "Approved" and glossary_term.get(
                    "name"
                ) == metadata_glossary_term.get("term"):
                    terms.append(
                        {
                            "guid": glossary_term.get("guid"),
                            "typeName": "AtlasGlossaryTerm",
                        }
                    )

        return terms
