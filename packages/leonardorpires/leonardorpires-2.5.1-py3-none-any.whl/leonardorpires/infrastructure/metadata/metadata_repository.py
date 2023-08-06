from typing import List, Optional, Union

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from pyiris.infrastructure.integration.database import Base, Default
from pyiris.infrastructure.integration.database.connection_factory import Session
from pyiris.infrastructure.metadata.metadata import MetadataTable as MetadataTableDomain


class MetadataTable(Default, Base):
    """
    A class to represent metadata table in database.
    ...
    """

    __tablename__ = "metadata_table"
    id = Column(UUIDType(), nullable=False, primary_key=True)
    name = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    team_owner = Column(String(), nullable=False)
    data_owner = Column(String(), nullable=False)
    data_expert = Column(String(), nullable=False)
    data_lake_zone = Column(String(), nullable=False)
    data_lake_path = Column(String(), nullable=False)
    permission = Column(String(), nullable=False)
    country = Column(String(), nullable=False)
    format = Column(String(), nullable=False)
    partition_by_column = Column(String(), nullable=True)
    repository = Column(String(), nullable=False)
    schema = relationship("MetadataTableSchema", cascade="all,delete,delete-orphan")

    @staticmethod
    def to_table(metadata):
        """
        Map metadata object to metadata database table object.
        :param metadata: The valid metadata object
        :type metadata: :class:`~pyiris.infrastructure.metadata.metadata_repository.MetadataTable`

        :return: The result of metadata database table object.
        :rtype metadata_table: :class:`~pyiris.infrastructure.metadata.metadata_repository.MetadataTable`
        """
        return MetadataTable(
            id=metadata.id,
            name=metadata.name,
            description=metadata.description,
            team_owner=metadata.team_owner,
            data_owner=metadata.data_owner,
            data_expert=metadata.data_expert,
            data_lake_zone=metadata.data_lake_zone,
            data_lake_path=metadata.data_lake_path,
            permission=metadata.permission,
            country=metadata.country,
            format=metadata.format,
            partition_by_column=metadata.partition_by_column,
            repository=metadata.repository,
            schema=list(map(MetadataTableSchema.to_table, metadata.schema)),
        )


class MetadataTableSchema(Default, Base):
    """
    A class to represent metadata table schema in database
    """

    __tablename__ = "metadata_table_schema"
    id = Column(UUIDType(), primary_key=True)
    metadata_table_id = Column(
        UUIDType(), ForeignKey(MetadataTable.id, ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)

    @staticmethod
    def to_table(metadata_schema):
        """
        Map metadata schema object to metadata schema database table object.
        :param metadata_schema: The valid metadata schema object
        :type metadata_schema: :class:`~pyiris.infrastructure.metadata.metadata_repository.MetadataTableSchema`

        :return: The results of metadata database table schema object.
        :rtype metadata_table_schema: :class:`~pyiris.infrastructure.metadata.metadata_repository.MetadataTableSchema`
        """
        return MetadataTableSchema(
            id=metadata_schema.id,
            metadata_table_id=metadata_schema.metadata_table_id,
            name=metadata_schema.name,
            type=metadata_schema.type,
            description=metadata_schema.description,
        )


class MetadataRepository(object):
    """
    A class responsible for execute CRUD operations in database.
    """

    def __init__(self, session=None) -> None:
        self.session: Optional[Session] = session or Session()

    def add(self, metadata: MetadataTableDomain):
        """
        Add metadata in database.
        :param metadata: The response from the request method.
        :type metadata: :class:`~pyiris.infrastructure.metadata.metadata_repository.MetadataTable`

        :return: The result of metadata database table object.
        :rtype metadata_table: :class:`~pyiris.infrastructure.metadata.metadata_repository.MetadataTable`
        """
        record = MetadataTable.to_table(metadata=metadata)
        self.session.add(record)
        return record

    def delete(self, repository: str) -> None:
        """
        Delete metadata from database based on the repository.
        :param repository: The repository name containing the metadata, used to filter the deletion.
        :type repository: string

        :return: None
        :rtype: None
        """
        self.session.query(MetadataTable).filter(
            MetadataTable.repository == repository
        ).delete()

    def list(self) -> Union[List[MetadataTableDomain], None]:
        """
        List all metadata table in database.
        :return: The results of metadata database tables object.
        :rtype list(metadata_table): :class:`~pyiris.infrastructure.metadata.metadata_repository.MetadataTable`
        """
        results = self.session.query(MetadataTable).all()
        if results:
            return results
        else:
            return None

    def load_by_table_name(self, name: str) -> Union[MetadataTable, None]:
        """
        Get the metadata table by filtering by name.
        :param name: The name of metadata table
        :type name: str

        :return: The result of metadata database table object.
        :rtype metadata_table: :class:`~pyiris.infrastructure.metadata.metadata_repository.MetadataTable`
        """
        result = (
            self.session.query(MetadataTable).filter(MetadataTable.name == name).first()
        )
        if result:
            return result
        else:
            return None
