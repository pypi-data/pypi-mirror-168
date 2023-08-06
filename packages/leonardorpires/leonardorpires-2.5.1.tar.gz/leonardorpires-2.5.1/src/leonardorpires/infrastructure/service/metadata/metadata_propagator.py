from typing import Dict, List, Optional

from pyiris.infrastructure.azure.purview.purview import Purview
from pyiris.infrastructure.integration.database.repository_integration import (
    RepositoryIntegration,
)
from pyiris.infrastructure.service.metadata.entity.dataset_metadata_entity import (
    DatasetMetadata,
)
from pyiris.infrastructure.service.metadata.entity.model_entity import Model
from pyiris.infrastructure.service.metadata.repository.dataset_metadata_repository import (
    DatasetMetadataRepository,
)
from pyiris.infrastructure.service.metadata.repository.model_repository import (
    ModelRepository,
)
from pyiris.infrastructure.service.monitor.log.logger import Logger

logger = Logger(__name__)


class MetadataPropagator(object):
    """
    This class intends to manage the metadata integrations, according to the choose strategy.

    :param purview_integration: the purview integration
    :type purview_integration: Optional, :class:
    `~pyiris.infrastructure.integration.database.repository_integration.RepositoryIntegration`.

    :param dataset_metadata_repository: the database repository integration
    :type dataset_metadata_repository: Optional, :class:
    `~pyiris.infrastructure.service.metadata.repository.dataset_metadata_repository.DatasetMetadataRepository`.
    """

    def __init__(
        self,
        purview_integration: Optional[Purview] = None,
        dataset_metadata_repository: Optional[RepositoryIntegration] = None,
        model_repository: Optional[ModelRepository] = None,
    ):
        self.purview_integration = purview_integration or Purview.build()
        self.dataset_metadata_repository = (
            dataset_metadata_repository or DatasetMetadataRepository()
        )
        self.model_repository = model_repository or ModelRepository()

    def to_source_integrations(
        self, purview_metadata: Dict, dataset_metadata: DatasetMetadata
    ) -> None:
        """
        This method is responsible for sending the metadata to source integrations: purview and metadata repository.

        :param purview_metadata: the purview metadata complete request.
        :type purview_metadata: dict

        :param dataset_metadata: the 'dataset_metadata' sqlalchemy declarative mapping object
        :type dataset_metadata: pyiris.infrastructure.service.metadata.entity.dataset_metadata.DatasetMetadataEntity
        """

        try:
            self.dataset_metadata_repository.add_if_not_exists(dataset_metadata)
            logger.info("Send metadata to Database with wsuccessfully.")

            self.purview_integration.create_entities(body=purview_metadata)
            logger.info("Send metadata to Purview with wsuccessfully.")
        except Exception as e:
            logger.error(message=repr(e))

    def to_intelligence_integrations(self, model_entities: List[Model]) -> None:
        """
        This method is responsible for sending the metadata to intelligence integrations:  metadata repository.

        :param model_entities: the list of 'model' sqlalchemy declrative mapping object.
        :type model_entities: list(pyiris.infrastructure.service.metadata.entity.model.Model)
        """

        for model_entity in model_entities:
            self.model_repository.add_if_not_exist(model=model_entity)
