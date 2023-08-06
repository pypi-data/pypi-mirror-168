from typing import Dict, List, Optional

from pyiris.infrastructure.azure.purview.purview import Purview
from pyiris.infrastructure.azure.purview.purview_mapper import PurviewMapper
from pyiris.infrastructure.integration.database.connection_factory import Session
from pyiris.infrastructure.metadata.metadata_mapper import MetadataMapper
from pyiris.infrastructure.metadata.metadata_repository import MetadataRepository
from pyiris.infrastructure.metadata.metadata_validator import MetadataValidator


class MetadataService(object):
    """
    A class responsible for orchestrating metadata components.

    :param metadata_validator: The metadata validator object.
    :type metadata_validator: :class:`~pyiris.infrastructure.metadata.metadata_validator.MetadataValidator`

    :param metadata_mapper: The metadata mapper object.
    :type metadata_mapper: :class:`~pyiris.infrastructure.metadata.metadata_mapper.MetadataMapper`

    :param purview_mapper: The metadata purview mapper object.
    :type purview_mapper: PurviewMapper :class:`~pyiris.infrastructure.azure.purview.purview_mapper.PurviewMapper`

    :param purview: The purview validator object.
    :type purview:  :class:`~pyiris.infrastructure.azure.purview.purview.Purview`

    :param metadata_repository: The metadata repository object.
    :type metadata_repository:  :class:`~pyiris.infrastructure.metadata.metadata_repository.MetadataRepository`

    """

    def __init__(
        self,
        metadata_validator: MetadataValidator,
        metadata_mapper: MetadataMapper,
        purview_mapper: PurviewMapper,
        purview: Purview,
        metadata_repository: MetadataRepository,
        session: Session,
    ):
        self.metadata_validator = metadata_validator or MetadataValidator()
        self.metadata_mapper = metadata_mapper or MetadataMapper()
        self.purview_mapper = purview_mapper or PurviewMapper()
        self.purview = purview or Purview.build()
        self.metadata_repository = metadata_repository or MetadataRepository()
        self.session = session or Session()

    def add(self, metadata: List[Dict]) -> None:
        """
        Validate metadata, mapping metadata to Purview request and create entities to your Purview backed Data Catalog.

        :param metadata: The list of metadata you want to create.
        :type metadata: dict

        :return: None
        :rtype: None
        """

        validated_metadata = self.validate_metadata(metadata)
        if validated_metadata:
            glossary_terms = self.purview.get_glossary_terms()
            purview_resource_set = self.purview_mapper.to_azure_resource_set_request(
                metadata=validated_metadata, glossary_terms=glossary_terms
            )
            self.purview.create_entities(body=purview_resource_set)

    def drop_and_add_to_db(self, metadata: List[Dict], repository: str) -> None:
        """
        Try to perform a deletion to the selected repository metadata.
        Try to validate, map to MetadataTable object and adding metadata to DB.

        :param metadata: The list of metadata you want to create.
        :type metadata: dict

        :param repository: The repository containing the metadata.
        :type repository: string

        :return: None
        :rtype: None
        """
        try:
            self.metadata_repository.delete(repository=repository)
            self.session.commit()
        except Exception as e:
            print(e)

        try:
            validated_metadata = self.validate_metadata(metadata)
            if validated_metadata:
                for metadata in validated_metadata:
                    metadata_table = self.metadata_mapper.to_domain(
                        metadata=metadata, repository=repository
                    )
                    self.metadata_repository.add(metadata=metadata_table)
            self.session.commit()
        except Exception as e:
            print(e)

    def validate_metadata(self, metadata: List[Dict]):
        validated_metadata = list(
            filter(
                lambda data: self.metadata_validator.validate(data).is_right(), metadata
            )
        )
        return validated_metadata

    @staticmethod
    def build(
        metadata_validator: Optional[MetadataValidator] = None,
        metadata_mapper: Optional[MetadataMapper] = None,
        purview_mapper: Optional[PurviewMapper] = None,
        purview: Optional[Purview] = None,
        metadata_repository: Optional[MetadataRepository] = None,
        session: Optional[Session] = None,
    ):
        """
        Build an Metadata Service Instance with all objects.

        :return: Metadata Service instance.
        :rtype: :class:`~pyiris.infrastructure.metadata.metadata_service.MetadataSerfvice`
        """

        return MetadataService(
            metadata_validator=metadata_validator,
            metadata_mapper=metadata_mapper,
            purview_mapper=purview_mapper,
            purview=purview,
            metadata_repository=metadata_repository,
            session=session,
        )
