from datetime import datetime

from pytz import timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from pyiris.infrastructure.integration.database import Base, Default


class DatasetMetadata(Base):
    """
    A class to represent dataset_metadata table in database.
    ...
    """

    __tablename__ = "dataset_metadata"
    id = Column(Integer(), nullable=False, primary_key=True)
    created_at = Column(
        DateTime(), default=datetime.now(timezone("Brazil/East")), nullable=False
    )
    updated_at = Column(
        DateTime(), onupdate=datetime.now(timezone("Brazil/East")), nullable=True
    )
    name = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    team_owner = Column(String(), nullable=False)
    data_owner = Column(String(), nullable=False)
    data_expert = Column(String(), nullable=False)
    data_lake_zone = Column(String(), nullable=False)
    data_lake_path = Column(String(), nullable=False)
    country = Column(String(), nullable=False)
    format = Column(String(), nullable=False)
    partition_by_column = Column(String(), nullable=True)
    schedule_interval = Column(String(), nullable=False)
    domain_type = Column(
        ENUM("SOURCE", "ANALYTICAL", name="domaintypeenum", create_type=True),
        nullable=False,
    )
    dataset_type = Column(
        ENUM(
            "TRANSACTIONAL",
            "METRIC",
            "MODEL",
            "DIMENSION",
            name="datasettypeenum",
            create_type=True,
        ),
        nullable=False,
    )

    schema = relationship("DatasetSchema", cascade="all,delete,delete-orphan")


class DatasetSchema(Base, Default):
    """
    A class to represent dataset_schema table in database
    """

    __tablename__ = "dataset_schema"
    id = Column(Integer, primary_key=True)
    dataset_metadata_id = Column(
        Integer(), ForeignKey(DatasetMetadata.id, ondelete="CASCADE")
    )
    name = Column(String(), nullable=False)
    type = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
