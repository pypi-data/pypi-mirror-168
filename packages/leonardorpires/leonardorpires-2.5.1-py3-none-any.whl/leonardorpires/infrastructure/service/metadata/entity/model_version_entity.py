from datetime import datetime

from pytz import timezone
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from pyiris.infrastructure.integration.database import Base


class ModelVersion(Base):
    """
    A class to represent algorithm model version table in database
    """

    __tablename__ = "model_version"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    created_at = Column(DateTime(), default=datetime.now(timezone("Brazil/East")))
    updated_at = Column(DateTime(), onupdate=datetime.now(timezone("Brazil/East")))
    model_id = Column(Integer(), ForeignKey("model.id", ondelete="CASCADE"))
    version = Column(Integer(), nullable=False)
    mlflow_registry = Column(String(), nullable=False)
    commit_hash = Column(String(), nullable=False)
    success_metric = Column(String(), nullable=True)
    metric_value = Column(Float(), nullable=True)
    model_input = Column(String(), nullable=False)
    model_output = Column(String(), nullable=False)
    mlflow_created_date = Column(DateTime(), nullable=False)
