from pyiris.infrastructure.integration.database.repository_integration import (
    RepositoryIntegration,
)
from pyiris.infrastructure.service.metadata.entity.dataset_metadata_entity import (
    DatasetMetadata,
)
from pyiris.infrastructure.service.monitor.log.logger import Logger

logger = Logger(__name__)


class DatasetMetadataRepository(RepositoryIntegration):
    """
    A class responsible for executing operations in database direct to
    pyiris.infrastructure.service.metadata.entity.dataset_metadata.DatasetMetadata table.
    """

    def __init__(self, session=None):
        super().__init__(session)

    @logger.log_decorator
    def add_if_not_exists(self, dataset_metadata: DatasetMetadata):
        current_table = (
            self.session.query(DatasetMetadata)
            .filter_by(
                name=dataset_metadata.name, team_owner=dataset_metadata.team_owner
            )
            .first()
        )
        if current_table:
            logger.info(
                f"Registry {dataset_metadata.name} already exists in the 'dataset_metadata' table, merge fields."
            )
            dataset_metadata.id = current_table.id
            self.session.merge(dataset_metadata)
            self.session.commit()
            return dataset_metadata

        result = self.add(table=dataset_metadata)
        logger.info(
            f"Registry {dataset_metadata.name} added to the 'dataset_metadata' table."
        )
        return result
