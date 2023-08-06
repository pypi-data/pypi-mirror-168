from typing import List, Optional

from pyiris.infrastructure.service.monitor.metric.metric import Metric
from pyiris.infrastructure.service.monitor.metric.metric_mapper import MetricMapper
from pyiris.infrastructure.service.monitor.metric.metric_propagator import (
    MetricPropagator,
)


class MetricService(object):
    def __init__(
        self,
        metric_propagator: Optional[MetricPropagator],
        metric_mapper: Optional[MetricMapper],
    ):
        self.metric_propagator = metric_propagator
        self.metric_mapper = metric_mapper

    def push_metrics(self, metrics: List[Metric]) -> None:
        datadog_metrics = self.metric_mapper.to_datadog_metrics(metrics=metrics)
        self.metric_propagator.propagate(datadog_metrics=datadog_metrics)

    @staticmethod
    def build(
        metric_propagator: Optional[MetricPropagator] = None,
        metric_mapper: Optional[MetricMapper] = None,
    ):
        metric_propagator = metric_propagator or MetricPropagator()
        metric_mapper = metric_mapper or MetricMapper()

        return MetricService(
            metric_propagator=metric_propagator, metric_mapper=metric_mapper
        )
