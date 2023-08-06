from pyiris.infrastructure.service.metadata.entity.dataset_metadata_entity import (
    DatasetMetadata,
)
from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.infrastructure.service.metadata.mapper.dataset_schema_mapper import (
    DatasetSchemaMapper,
)
from pyiris.ingestion.enums.enums import (
    DatasetType,
    DomainType,
    FileFormats,
    IrisMountNames,
)
from pyiris.ingestion.task.entity.task_entity import TaskEntity


class DatasetMetadataMapper(object):
    """
    This class intends to map the metadata dict to a declarative base sqlalchemy object representing 'dataset_metadata'
    table.
    """

    @staticmethod
    def to_model(task_entity: TaskEntity, metadata_entity: MetadataEntity):
        return DatasetMetadata(
            name=task_entity.name,
            description=metadata_entity.description,
            team_owner=task_entity.owner_team,
            data_owner=task_entity.task_owner,
            data_expert=metadata_entity.dataexpert,
            data_lake_zone=IrisMountNames.TRUSTEDZONE.value,
            data_lake_path=task_entity.path,
            country=task_entity.country,
            format=task_entity.format or FileFormats.DELTA.value,
            partition_by_column=task_entity.partition_by,
            schedule_interval=task_entity.schedule_interval,
            domain_type=DomainType.SOURCE.name,
            dataset_type=DatasetType.TRANSACTIONAL.name,
            schema=list(map(DatasetSchemaMapper.to_table, metadata_entity.schema)),
        )
