from typing import Dict, List, Optional

from pyiris.infrastructure.integration.datadog.datadog import DataDog


class MetricPropagator(object):
    def __init__(self, datadog: Optional[DataDog] = None):
        self.datadog = datadog or DataDog()

    def propagate(self, datadog_metrics: List[Dict]):
        self.datadog.send_metrics(metrics=datadog_metrics)
