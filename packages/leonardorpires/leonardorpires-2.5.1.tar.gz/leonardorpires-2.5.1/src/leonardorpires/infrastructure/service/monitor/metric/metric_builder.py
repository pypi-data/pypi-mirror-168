from abc import abstractmethod
from typing import Optional

from pyspark.sql import DataFrame

from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.infrastructure.service.monitor.metric.metric import Metric, MetricType, Tag
from pyiris.ingestion.task.entity.task_entity import TaskEntity


class MetricBuilder(object):
    @staticmethod
    @abstractmethod
    def build(self):
        pass


class ExecutionMetrics(MetricBuilder):
    @staticmethod
    def build(
        task_entity: Optional[TaskEntity] = None,
        metadata_entity: Optional[MetadataEntity] = None,
        task_execution_status: Optional[int] = None,
        elapsed_time: Optional[int] = None,
        dataframe: Optional[DataFrame] = None,
    ):
        tag = Tag(
            task_name=task_entity.name,
            task_owner=task_entity.task_owner,
            owner_team=task_entity.owner_team,
            data_owner=metadata_entity.dataexpert,
            source_system=task_entity.system,
            country=task_entity.country,
        )

        metrics = [
            Metric(
                name="iris.task.execution.status",
                value=task_execution_status,
                metric_type=MetricType.COUNT.value,
                tag=tag,
            ),
            Metric(
                name="iris.task.execution.elapsed_time",
                value=elapsed_time,
                metric_type=MetricType.COUNT.value,
                tag=tag,
            ),
            Metric(
                name="iris.task.dataset.total_rows",
                value=dataframe.count() if dataframe else 0,
                metric_type=MetricType.COUNT.value,
                tag=tag,
            ),
        ]

        return metrics
