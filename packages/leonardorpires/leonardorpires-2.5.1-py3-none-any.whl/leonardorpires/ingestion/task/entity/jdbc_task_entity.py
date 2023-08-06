import json
from typing import Dict, Optional

from pyiris.infrastructure.common.exception import ReaderOptionsDatabaseException
from pyiris.ingestion.enums.enums import JdbcDatabaseOptions
from pyiris.ingestion.task.entity.task_entity import TaskEntity


class JdbcTaskEntity(TaskEntity):
    """
    This class represents the JDBC task entity on source tasks.

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

    :param name: the name of the dataset
    :type name: string

    :param task_owner: the name of the dataset owner
    :type task_owner: string

    :param owner_team: the team that owns to the dataset
    :type owner_team: string

    :param database_type: the type of the database
    :type database_type: string

    :param database_name: name of the database
    :type database_name: string

    :param host: the host for the jdbc connection
    :type host: string

    :param columns: the columns of the dataset to be ingested. Can be "*" to indicate all columns
    :type columns: string

    :param schema: the schema of the dataset to be ingested
    :type schema: string

    :param login: the login for the jdbc connection
    :type login: string

    :param password: the password for the jdbc connection
    :type password: string

    :param notifier: the alert definitions
    :type notifier: pyiris.infrastructure.monitor.notifier.Notifier

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

    :param filter: the sql filter for the ingested dataset.
    I.e.: filter = "testfield = 'test'"
    :type filter: Optional, string

    :param backfill: the backfill argument for the ingested dataset backfill filter
    I.e.: backfill = {"filter_column": "test_column"}
    :type backfill: Optional, dict

    :param execution_date: the execution_date argument for the ingested dataset backfill filter
    I.e.: execution_date = "2020-01-01"
    :type execution_date: Optional, string

    :param prev_execution_date: the prev_execution_date argument for the ingested dataset backfill filter
    I.e.: prev_execution_date = "2019-01-01"
    :type prev_execution_date: Optional, string

    :param jdbc_reader_options: all allowed spark jdbc read extra options
    :type jdbc_reader_options: required, dict

    :param base_path: the base path to write the task files
    :type base_path: Optional, string

    :param extra: the extra configurations for the JDBC connections
    :type extra: str

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
        task_owner: str,
        owner_team: str,
        database_type: str,
        database_name: str,
        host: str,
        columns: str,
        schema: str,
        login: str,
        password: str,
        notifier: dict,
        extra: str,
        options: Optional[Dict] = None,
        sync_mode: Optional[str] = None,
        transformations: Optional[Dict] = None,
        partition_by: Optional[str] = None,
        format: Optional[str] = None,
        permission: Optional[str] = None,
        filter: Optional[str] = None,
        backfill: Optional[Dict] = None,
        execution_date: Optional[str] = None,
        prev_execution_date: Optional[str] = None,
        jdbc_reader_options: Optional[dict] = None,
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
        self.database_type = database_type
        self.database_name = database_name
        self.base_path = base_path
        self.host = host
        self.columns = columns
        self.schema = schema
        self.login = login
        self.password = password
        self.filter = filter
        self.backfill = backfill
        self.extra = extra
        self.execution_date = execution_date
        self.prev_execution_date = prev_execution_date
        self.jdbc_reader_options = jdbc_reader_options
        self.connection_string = None
        self.query = None

    @property
    def name(self) -> str:
        return self._name.lower()

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @property
    def connection_string(self) -> str:
        if self.database_type == JdbcDatabaseOptions.SQLSERVER.value:
            return f"jdbc:{self.database_type}://{self.host}"
        elif self.database_type == JdbcDatabaseOptions.MYSQL.value:
            return f"jdbc:{self.database_type}://{self.host}/"
        elif self.database_type == JdbcDatabaseOptions.POSTGRESQL.value:
            return f"jdbc:{self.database_type}://{self.host}/{self.database_name}"
        else:
            raise Exception(f"The database type {self.database_type} is not supported")

    @connection_string.setter
    def connection_string(self, value) -> None:
        self._connection_string = value

    @property
    def jdbc_reader_options(self) -> dict:
        database = {
            "driver": self.__spark_reader_driver(),
            "database": self.database_name,
        }
        return database

    @jdbc_reader_options.setter
    def jdbc_reader_options(self, value) -> None:
        self._jdbc_reader_options = value

    def __spark_reader_driver(self) -> str:
        if self.database_type == JdbcDatabaseOptions.SQLSERVER.value:
            return "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        elif self.database_type == JdbcDatabaseOptions.MYSQL.value:
            return "com.mysql.cj.jdbc.Driver"
        elif self.database_type == JdbcDatabaseOptions.POSTGRESQL.value:
            return "org.postgresql.Driver"
        else:
            raise ReaderOptionsDatabaseException(
                f"The database type {self.database_type} is not supported"
            )

    @property
    def query(self) -> str:
        if self.filter and not self.backfill:
            return f"select {self.columns} from {self.schema}.{self.name} where {self.filter}"
        elif self.backfill and not self.filter:
            filter_column = self.backfill.get("filter_column")
            return f"select {self.columns} from {self.schema}.{self.name} where {filter_column} >= '{self.execution_date}' and {filter_column} < '{self.prev_execution_date}'"
        elif not self.filter and not self.backfill:
            return f"select {self.columns} from {self.schema}.{self.name}"

    @query.setter
    def query(self, value) -> None:
        self._query = value

    @property
    def database_name(self) -> str:
        if not self._database_name:
            return json.loads(self.extra).get("database_name")
        else:
            return self._database_name

    @database_name.setter
    def database_name(self, value) -> None:
        self._database_name = value

    @staticmethod
    def build(context: dict):
        return JdbcTaskEntity(
            dag_id=context.get("dag_id"),
            dag_class=context.get("dag_class"),
            dag_type=context.get("dag_type"),
            schedule_interval=context.get("schedule_interval"),
            system=context.get("system"),
            country=context.get("country"),
            name=context.get("datasets").get("name"),
            task_owner=context.get("datasets").get("task_owner"),
            owner_team=context.get("datasets").get("owner_team"),
            sync_mode=context.get("datasets").get("mode"),
            database_type=context.get("datasets").get("database_type"),
            database_name=context.get("datasets").get("database_name"),
            host=context.get("host"),
            columns=context.get("datasets").get("columns"),
            schema=context.get("datasets").get("schema"),
            base_path=context.get("base_path"),
            login=context.get("login"),
            password=context.get("password"),
            transformations=context.get("datasets").get("transformations"),
            notifier=context.get("datasets").get("notifier"),
            options=context.get("datasets").get("options"),
            partition_by=context.get("datasets").get("partition_by"),
            format=context.get("datasets").get("format"),
            permission=context.get("datasets").get("permission"),
            filter=context.get("datasets").get("filter"),
            backfill=context.get("datasets").get("backfill"),
            execution_date=context.get("execution_date"),
            prev_execution_date=context.get("prev_execution_date"),
            extra=context.get("extra"),
        )
