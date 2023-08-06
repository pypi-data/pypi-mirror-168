import json
from typing import Dict, Optional

from pyiris.infrastructure.common.helper import Helper
from pyiris.ingestion.task.entity.task_entity import TaskEntity


class RabbitMQTaskEntity(TaskEntity):
    """
    This class represents the RabbitMQ task entity on source tasks.

    :param dag_id: the name of the dag
    :type dag_id: string

    :param dag_class: the class of the dag
    :type dag_class: string

    :param dag_type: the type of the dag
    :type dag_type: string

    :param schedule_interval: the dataset scheduler interval
    :type schedule_interval: string

    :param system: the name system providing the data
    :type system: string

    :param country: the country related to the dataset
    :type country: string

    :param name: the name of the rabbitMQ queue
    :type name: string

    :param task_owner: the name of the dataset owner
    :type task_owner: string

    :param owner_team: the team that owns to the dataset
    :type owner_team: string

    :param notifier: the alert definitions
    :type notifier: pyiris.infrastructure.monitor.notifier.notifier

    :param host: the host for the RabbitMQ connection
    :type host: string

    :param schema: the schema for the RabbitMQ connection
    :type schema: string

    :param login: the login for the RabbitMQ connection
    :type login: string

    :param password: the password for the RabbitMQ connection
    :type password: string

    :param port: the port for the RabbitMQ connection
    :type port: string

    :param extra: the extra configurations for the RabbitMQ connection
    :type extra: str

    :param execution_timeout: the execution timeout for the RabbitMQ connection
    :type execution_timeout: Optional, integer

    :param transformations: the data transformations definitions of the source-rawzone dataset.
    The allowed transformations are: hash and drop_duplicate.
    To enable this transformations, a dict have to be passed with this way:
        transformations = {'hash': {'from_columns': ['teste', 'teste2']}}
        transformations = {'drop_duplicate': {'based_on_columns': ['test']}
        transformations = {'drop_duplicate': {'exclude_only': ['test2']}}
    :type transformations: optional, dict

    :param partition_by: the column to partition the files in the data lake
    :type partition_by: optional, string

    :param format: the spark file format. Default "delta".
    :type format: optional, string

    :param permission: the data lake permission. May be public or private.
    :type permission: Optional, string, allowed only private or public.

    :param base_path: the base path to write the task files
    :type base_path: Optional, string

    :param sync_mode: the write mode to save files in the rawzone, allowed overwrite and append
    :type sync_mode: string, optional.

    :param options: an allowed spark write option
    :type options: dict, optional.
    """

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
        extra: str,
        sync_mode: Optional[str] = None,
        options: Optional[Dict] = None,
        vhost: Optional[str] = None,
        port: Optional[str] = None,
        schema: Optional[str] = None,
        execution_timeout: Optional[int] = None,
        prefetch_count: Optional[int] = None,
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
        self.schema = schema
        self.login = login
        self.password = password
        self.port = port
        self.vhost = vhost
        self.extra = extra
        self.domain = domain
        self.entity = entity
        self.base_path = base_path
        self.execution_timeout = execution_timeout
        self.prefetch_count = prefetch_count

    @property
    def name(self) -> str:
        return self._name.upper()

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
    def execution_timeout(self) -> int:
        if not self._execution_timeout:
            return 60
        else:
            return self._execution_timeout

    @execution_timeout.setter
    def execution_timeout(self, value) -> None:
        self._execution_timeout = value

    @property
    def prefetch_count(self) -> int:
        if not self._prefetch_count:
            return 10000
        else:
            return self._prefetch_count

    @prefetch_count.setter
    def prefetch_count(self, value) -> None:
        self._prefetch_count = value

    @property
    def vhost(self) -> str:
        if not self._vhost:
            return json.loads(self.extra).get("vhost")
        else:
            return self._vhost

    @vhost.setter
    def vhost(self, value) -> None:
        self._vhost = value

    @staticmethod
    def build(context: dict):
        return RabbitMQTaskEntity(
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
            sync_mode=context.get("datasets").get("sync_mode"),
            transformations=context.get("datasets").get("transformations"),
            execution_timeout=context.get("datasets").get("execution_timeout"),
            prefetch_count=context.get("datasets").get("prefetch_count"),
            notifier=context.get("datasets").get("notifier"),
            options=context.get("datasets").get("options"),
            partition_by=context.get("datasets").get("partition_by"),
            format=context.get("datasets").get("format"),
            permission=context.get("datasets").get("permission"),
            base_path=context.get("base_path"),
            host=context.get("host"),
            schema=context.get("schema"),
            login=context.get("login"),
            password=context.get("password"),
            port=context.get("port"),
            vhost=context.get("vhost"),
            extra=context.get("extra"),
        )
