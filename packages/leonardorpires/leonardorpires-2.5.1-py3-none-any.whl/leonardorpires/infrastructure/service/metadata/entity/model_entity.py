from datetime import datetime

from pytz import timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from pyiris.infrastructure.integration.database import Base
from pyiris.infrastructure.service.metadata.entity.dataset_metadata_entity import (
    DatasetMetadata,
)
from pyiris.infrastructure.service.metadata.entity.model_version_entity import (
    ModelVersion,
)


class Model(Base):
    """
    A class to represent algorithm model table in database
    """

    __tablename__ = "model"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now(timezone("Brazil/East")))
    updated_at = Column(DateTime(), onupdate=datetime.now(timezone("Brazil/East")))
    description = Column(String(), nullable=False)
    deployment_flavor = Column(String(), nullable=False)
    repository = Column(String(), nullable=False)
    project_docs_url = Column(String(), nullable=False)
    dataset_metadata_id = Column(
        Integer(), ForeignKey(DatasetMetadata.id, ondelete="CASCADE")
    )

    versions = relationship(
        ModelVersion,
        primaryjoin=id == ModelVersion.model_id,
        cascade="all,delete,delete-orphan",
    )
