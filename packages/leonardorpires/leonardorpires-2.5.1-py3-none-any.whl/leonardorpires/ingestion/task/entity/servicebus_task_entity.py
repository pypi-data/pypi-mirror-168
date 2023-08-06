from typing import Dict, Optional

from pyiris.infrastructure.common.helper import Helper
from pyiris.ingestion.task.entity.task_entity import TaskEntity


class ServiceBusTaskEntity(TaskEntity):
    def __init__(
        self,
        dag_id: str,
        dag_class: str,
        dag_type: str,
        schedule_interval: str,
        system: str,
        country: str,
        name: str,
        domain: str,
        entity: str,
        task_owner: str,
        owner_team: str,
        notifier: dict,
        host: str,
        login: str,
        password: str,
        extra: Optional[str] = None,
        options: Optional[Dict] = None,
        sync_mode: Optional[str] = None,
        max_message_count: Optional[int] = None,
        max_wait_time: Optional[int] = None,
        max_lock_renewal_duration: Optional[int] = None,
        transformations: Optional[Dict] = None,
        partition_by: Optional[str] = None,
        format: Optional[str] = None,
        permission: Optional[str] = None,
        base_path: Optional[str] = None,
    ):
        super().__init__(
            dag_id,
            dag_class,
            dag_type,
            schedule_interval,
            system,
            country,
            name,
            task_owner,
            owner_team,
            notifier,
            options,
            sync_mode,
            transformations,
            partition_by,
            format,
            permission,
            base_path,
        )

        self.host = host
        self.login = login
        self.password = password
        self.extra = extra
        self.domain = domain
        self.entity = entity
        self.max_message_count = max_message_count
        self.max_wait_time = max_wait_time
        self.max_lock_renewal_duration = max_lock_renewal_duration
        self.base_path = base_path
        self.connection_string = None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @property
    def path(self) -> str:
        return f"{Helper.camel_case(string=self.system)}/{Helper.camel_case(string=self.domain)}/{Helper.camel_case(string=self.entity)}"

    @path.setter
    def path(self, value) -> None:
        self._path = value

    @property
    def max_message_count(self) -> int:
        if not self._max_message_count:
            return 10000
        else:
            return self._max_message_count

    @max_message_count.setter
    def max_message_count(self, value) -> None:
        self._max_message_count = value

    @property
    def max_wait_time(self) -> float:
        if not self._max_wait_time:
            return 60
        else:
            return self._max_wait_time

    @max_wait_time.setter
    def max_wait_time(self, value) -> None:
        self._max_wait_time = value

    @property
    def max_lock_renewal_duration(self) -> int:
        if not self._max_wait_time:
            return 600
        else:
            return self._max_wait_time

    @max_lock_renewal_duration.setter
    def max_lock_renewal_duration(self, value) -> None:
        self._max_wait_time = value

    @property
    def connection_string(self) -> str:
        return f"Endpoint=sb://{self.host}/;SharedAccessKeyName={self.login};SharedAccessKey={self.password}"

    @connection_string.setter
    def connection_string(self, value) -> None:
        self._connection_string = value

    @staticmethod
    def build(context: dict):
        return ServiceBusTaskEntity(
            dag_id=context.get("dag_id"),
            dag_class=context.get("dag_class"),
            dag_type=context.get("dag_type"),
            schedule_interval=context.get("schedule_interval"),
            system=context.get("system"),
            country=context.get("country"),
            name=context.get("datasets").get("name"),
            domain=context.get("datasets").get("domain"),
            entity=context.get("datasets").get("entity"),
            task_owner=context.get("datasets").get("task_owner"),
            owner_team=context.get("datasets").get("owner_team"),
            notifier=context.get("datasets").get("notifier"),
            options=context.get("datasets").get("options"),
            sync_mode=context.get("datasets").get("sync_mode"),
            max_message_count=context.get("datasets").get("max_message_count"),
            max_wait_time=context.get("datasets").get("max_wait_time"),
            transformations=context.get("datasets").get("transformations"),
            partition_by=context.get("datasets").get("partition_by"),
            format=context.get("datasets").get("format"),
            base_path=context.get("base_path"),
            host=context.get("host"),
            login=context.get("login"),
            password=context.get("password"),
            extra=context.get("extra"),
        )
