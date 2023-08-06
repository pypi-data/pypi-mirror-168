import time
import traceback

from pyiris.infrastructure.common.exception import PyIrisTaskException
from pyiris.infrastructure.common.feature_flag import FeatureFlag
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.service.monitor.metric.metric_builder import ExecutionMetrics
from pyiris.infrastructure.service.monitor.notifier.notifier_service import (
    NotifierService,
)
from pyiris.ingestion.enums.enums import TaskExecutionStatus

logger = Logger(__name__)


class TaskDecorator(object):
    def __call__(self, func):
        def run(*args):
            dataframe = None
            elapsed_time: float = 0
            task_execution_status = TaskExecutionStatus.SUCCESS.value

            try:
                start = time.time()
                dataframe = func(*args)
                elapsed_time = time.time() - start
            except Exception as message:
                task_execution_status = TaskExecutionStatus.FAILED.value
                notifier_service = NotifierService(
                    task_entity=args[0].task_entity,
                    metadata_entity=args[0].metadata_entity,
                )

                notifier_service.on_error(
                    error_message=repr(message), traceback=traceback.format_exc()
                )
                raise PyIrisTaskException(message=message)

            finally:
                if FeatureFlag.metadata_service_is_enable():
                    from pyiris.infrastructure.service.metadata.metadata_service import (
                        MetadataService,
                    )

                    metadata_service = MetadataService.build()
                    metadata_service.send_to_source_integrations(
                        task_entity=args[0].task_entity,
                        metadata_entity=args[0].metadata_entity,
                    )

                if FeatureFlag.metric_service_is_enable():
                    from pyiris.infrastructure.service.monitor.metric.metric_service import (
                        MetricService,
                    )

                    metrics = ExecutionMetrics.build(
                        task_entity=args[0].task_entity,
                        metadata_entity=args[0].metadata_entity,
                        task_execution_status=task_execution_status,
                        elapsed_time=int(elapsed_time),
                        dataframe=dataframe,
                    )

                    metric_service = MetricService.build()
                    metric_service.push_metrics(metrics=metrics)

        return run
