from distutils.util import strtobool

from pyiris.infrastructure.common.config import get_key
from pyiris.infrastructure.service.monitor.log.logger import Logger

logger = Logger(__name__)


class FeatureFlag(object):
    @staticmethod
    def metadata_service_is_enable():
        result = get_key("FeatureFlagMetadataService")
        if strtobool(result):
            logger.info("Metadata Service is enable!")
            return True
        else:
            logger.info("Metadata Service is not enable!")
            return False

    @staticmethod
    def metric_service_is_enable():
        result = get_key("FeatureFlagMetricService")
        if strtobool(result):
            logger.info("Metric Service is enable!")
            return True
        else:
            logger.info("Metric Service is not enable!")
            return False
