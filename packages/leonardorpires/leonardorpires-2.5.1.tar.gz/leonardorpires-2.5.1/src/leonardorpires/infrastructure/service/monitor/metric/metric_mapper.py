from typing import List

from pyiris.infrastructure.service.monitor.metric.metric import Metric, Tag


class MetricMapper(object):
    @staticmethod
    def to_datadog_metrics(metrics: List[Metric]):
        return list(map(MetricMapper.to_datadog_metric, metrics))

    @staticmethod
    def to_datadog_metric(metric: Metric):
        return {
            "metric": metric.name,
            "type": metric.metric_type,
            "points": metric.value,
            "tags": MetricMapper.to_datadog_tag(metric.tag),
        }

    @staticmethod
    def to_datadog_tag(tag: Tag):
        return [
            f"task_name:{tag.task_name}",
            f"owner_team:{tag.owner_team}",
            f"data_owner:{tag.data_owner}",
            f"source_system:{tag.source_system}",
            f"country:{tag.country}",
        ]
