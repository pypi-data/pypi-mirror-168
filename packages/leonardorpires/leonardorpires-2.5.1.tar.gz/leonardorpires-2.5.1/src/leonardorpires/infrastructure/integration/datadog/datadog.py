from typing import Dict, List

from datadog import api, initialize

from pyiris.infrastructure.common.config import get_key
from pyiris.infrastructure.common.exception import DataDogFailedSendMetricsException
from pyiris.infrastructure.service.monitor.log.logger import Logger

logger = Logger(__name__)


class DataDog(object):
    def __init__(self, api_key: str = None, app_key: str = None):
        self.api_key = api_key or get_key("datadogApiKey")
        self.app_key = app_key or get_key("datadogAppKey")
        self.options = {"api_key": self.api_key, "app_key": self.app_key}

        initialize(**self.options)

    @staticmethod
    def send_metrics(metrics: List[Dict]):
        result = api.Metric.send(metrics=metrics)
        if result["status"] == "ok":
            logger.info("Propagated metrics to DataDog with successfully.")
            return result
        else:
            raise DataDogFailedSendMetricsException(message=result["errors"])
