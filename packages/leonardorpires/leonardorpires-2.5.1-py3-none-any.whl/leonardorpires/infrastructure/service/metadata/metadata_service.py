from typing import Dict, List, Optional

from pyiris.infrastructure.azure.purview.purview import Purview
from pyiris.infrastructure.azure.purview.purview_mapper import PurviewMapper
from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.infrastructure.service.metadata.mapper.dataset_metadata_mapper import (
    DatasetMetadataMapper,
)
from pyiris.infrastructure.service.metadata.mapper.model_mapper import ModelMapper
from pyiris.infrastructure.service.metadata.metadata_propagator import (
    MetadataPropagator,
)
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.task.entity.task_entity import TaskEntity

logger = Logger(__name__)


class MetadataService(object):
    """
    This class is responsible for orchestrating the metadata propagations.

    :param metadata_propagator: the class responsible for the propagations integrations.
    :type metadata_propagator: Optional, :class: `pyiris.infrastructure.service.metadata.metadata_propagator.MetadataPropagator`

    :param dataset_metadata_mapper: the 'dataset_metadata' mapper.
    :type dataset_metadata_mapper: Optional, :class:
    `pyiris.infrastructure.service.metadata.mapper.dataset_metadata_mapper.DatasetMetadataMapper`

    :param purview_mapper: the purview full request mapper.
    :type purview_mapper: Optional, :class: `pyiris.infrastructure.azure.purview.purview_mapper.PurviewMapper`

    :param purview_integration: the purview integration.
    :type purview_integration: Optional, :class: `pyiris.infrastructure.azure.purview.purview.Purview`

    :param model_mapper: the 'model' mapper
    """

    def __init__(
        self,
        model_mapper: Optional[ModelMapper] = None,
        metadata_propagator: Optional[MetadataPropagator] = None,
        dataset_metadata_mapper: Optional[DatasetMetadataMapper] = None,
        purview_mapper: Optional[PurviewMapper] = None,
        purview_integration: Optional[Purview] = None,
    ):
        self.dataset_metadata_mapper = (
            dataset_metadata_mapper or DatasetMetadataMapper()
        )
        self.model_mapper = model_mapper or ModelMapper()
        self.purview_mapper = purview_mapper or PurviewMapper()
        self.metadata_propagator = metadata_propagator or MetadataPropagator()
        self.purview_integration = purview_integration or Purview.build()

    def send_to_source_integrations(
        self, task_entity: TaskEntity, metadata_entity: MetadataEntity
    ) -> None:
        """
        This method is responsible for sending the source metadata objects/requests to metadata propagator.

        :param task_entity: the respective task entity.
        :type task_entity: TaskEntity

        :param metadata_entity: the respective metadata entity.
        :type metadata_entity: MetadataEntity
        """
        glossary_terms = self.purview_integration.get_glossary_terms()
        purview_metadata = self.purview_mapper.to_azure_resource_set_request_by_object(
            task_entity=task_entity,
            metadata_entity=metadata_entity,
            glossary_terms=glossary_terms,
        )

        dataset_metadata = self.dataset_metadata_mapper.to_model(
            task_entity=task_entity, metadata_entity=metadata_entity
        )
        self.metadata_propagator.to_source_integrations(
            purview_metadata=purview_metadata, dataset_metadata=dataset_metadata
        )

    def send_to_intelligence_integrations(
        self,
        model_definition: Dict,
        product_definition: Dict,
        project_metadata: List,
        model_definition_path,
    ) -> None:
        """
        This method is responsible for sending the intelligence metadata objects/requests to metadata propagator.

        :param model_definition: the dict with the model definition parameters.
        :type Dict

        :param product_definition: the dict with the product_definition parameters.
        :type Dict

        :param project_metadata: the list with the project metadata parameters.
        :type List

        :param model_definition_path: the path of model_definition file to get last commit
        """

        model_entities = self.model_mapper.to_entities(
            model_definition=model_definition,
            product_definition=product_definition,
            project_metadata=project_metadata,
            model_definition_path=model_definition_path,
        )

        self.metadata_propagator.to_intelligence_integrations(
            model_entities=model_entities
        )

    @staticmethod
    def build():
        purview_integration = Purview.build()
        metadata_propagator = MetadataPropagator(
            purview_integration=purview_integration
        )
        dataset_metadata_mapper = DatasetMetadataMapper()
        purview_mapper = PurviewMapper()

        return MetadataService(
            dataset_metadata_mapper=dataset_metadata_mapper,
            purview_mapper=purview_mapper,
            metadata_propagator=metadata_propagator,
            purview_integration=purview_integration,
        )
