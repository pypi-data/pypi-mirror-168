from functools import reduce
from typing import Optional, Union

from pyspark.sql.session import SparkSession

from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.ingestion.enums.enums import TaskType
from pyiris.ingestion.task.base_task import BaseTask
from pyiris.ingestion.task.entity.file_system_task_entity import FileSystemTaskEntity
from pyiris.ingestion.task.entity.jdbc_task_entity import JdbcTaskEntity
from pyiris.ingestion.task.entity.rabbitmq_task_entity import RabbitMQTaskEntity
from pyiris.ingestion.task.entity.restapi_task_entity import RestApiTaskEntity
from pyiris.ingestion.task.entity.servicebus_task_entity import ServiceBusTaskEntity
from pyiris.ingestion.task.entity.sharepoint_task_entity import SharepointTaskEntity
from pyiris.ingestion.task.source_tasks.file_system_task import FileSystemTask
from pyiris.ingestion.task.source_tasks.jdbc_task import JdbcTask
from pyiris.ingestion.task.source_tasks.rabbitmq_task import RabbitMQTask
from pyiris.ingestion.task.source_tasks.restapi_task import RestApiTask
from pyiris.ingestion.task.source_tasks.servicebus_task import ServiceBusTask
from pyiris.ingestion.task.source_tasks.sharepoint_task import SharePointTask


class TaskEntryPoint(object):
    def __init__(self, context: dict, engine: Optional[SparkSession] = None):
        self.context = context
        self.engine = engine
        self.task_builders = [
            RabbitMQTaskBuilder(),
            JdbcTaskBuilder(),
            SharepointTaskBuilder(),
            FileSystemTaskBuilder(),
            RestApiTaskBuilder(),
            ServiceBusTaskBuilder(),
        ]

    def handle(self):
        result = reduce(
            lambda context, builder: builder.build(context, engine=self.engine)
            if not isinstance(context, BaseTask)
            else context,
            self.task_builders,
            self.context,
        )
        return result


class ServiceBusTaskBuilder:
    @staticmethod
    def build(context: dict, engine: SparkSession) -> Union[ServiceBusTask, dict]:
        if context.get("dag_type") == TaskType.SERVICEBUS.value:
            return ServiceBusTask.build(
                task_entity=ServiceBusTaskEntity.build(context=context),
                metadata_entity=MetadataEntity.build(
                    metadata=context.get("datasets").get("metadata")
                ),
                engine=engine,
            )
        else:
            return context


class RabbitMQTaskBuilder(object):
    @staticmethod
    def build(context: dict, engine: SparkSession) -> Union[RabbitMQTask, dict]:
        if context.get("dag_type") == TaskType.RABBITMQ.value:
            return RabbitMQTask.build(
                task_entity=RabbitMQTaskEntity.build(context=context),
                metadata_entity=MetadataEntity.build(
                    metadata=context.get("datasets").get("metadata")
                ),
                engine=engine,
            )
        else:
            return context


class JdbcTaskBuilder(object):
    @staticmethod
    def build(context: dict, engine: SparkSession) -> Union[JdbcTask, dict]:
        if context.get("dag_type") == TaskType.JDBC.value:
            return JdbcTask.build(
                task_entity=JdbcTaskEntity.build(context),
                metadata_entity=MetadataEntity.build(
                    metadata=context.get("datasets").get("metadata")
                ),
                engine=engine,
            )
        else:
            return context


class SharepointTaskBuilder(object):
    @staticmethod
    def build(context: dict, engine: SparkSession) -> Union[SharePointTask, dict]:
        if context.get("dag_type") == TaskType.SHAREPOINT.value:
            return SharePointTask.build(
                task_entity=SharepointTaskEntity.build(context=context),
                metadata_entity=MetadataEntity.build(
                    metadata=context.get("datasets").get("metadata")
                ),
                engine=engine,
            )
        else:
            return context


class FileSystemTaskBuilder(object):
    @staticmethod
    def build(context: dict, engine: SparkSession) -> Union[FileSystemTask, dict]:
        if context.get("dag_type") == TaskType.FILESYSTEM.value:
            return FileSystemTask.build(
                task_entity=FileSystemTaskEntity.build(context),
                metadata_entity=MetadataEntity.build(
                    metadata=context.get("datasets").get("metadata")
                ),
                engine=engine,
            )
        else:
            return context


class RestApiTaskBuilder(object):
    @staticmethod
    def build(context: dict, engine: SparkSession) -> Union[RestApiTask, dict]:
        if context.get("dag_type") == TaskType.RESTAPI.value:
            return RestApiTask.build(
                task_entity=RestApiTaskEntity.build(context=context),
                metadata_entity=MetadataEntity.build(
                    metadata=context.get("datasets").get("metadata")
                ),
                engine=engine,
            )
        else:
            return context
