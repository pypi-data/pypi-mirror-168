from typing import Dict, Optional

from pyiris.ingestion.task.entity.task_entity import TaskEntity


class FileSystemTaskEntity(TaskEntity):
    """
    This class represents the File System task entity on source tasks.

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

    :param notifier: the alert definitions
    :type notifier: pyiris.infrastructure.monitor.notifier.Notifier

    :param host: the host for the filesystem connection
    :type host: string

    :param username: the username for the filesystem connection
    :type username: string

    :param password: the password for the filesystem connection
    :type password: string

    :param file_path: the file path location the filesystem
    :type file_path: string

    :param column_separator: the column separator characther for the file
    :type column_separator: string

    :param has_header: a boolean indicating if the file has a header
    :type has_header: boolean

    :param file_type: What is the file format. Defaults to CSV
    :type file_type: Optional, str

    :param encoding: If the user desires to read the file with some encoding. Defaults to utf-8
    :type encoding: Optional, str

    :param mode: How to actually read the file. Defaults to "r" as in "read". The user might also choose
    to read as a binary, for example, with "rb". Should mostly be changed when working with text files
    :type mode: Optional, str

    :param newline: How to identify a line break. Defaults to "\n"
    :type newline: Optional, str

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
        task_owner: str,
        owner_team: str,
        notifier: dict,
        host: str,
        username: str,
        password: str,
        file_path: str,
        column_separator: str,
        has_header: bool,
        sync_mode: Optional[str] = None,
        file_type: Optional[str] = None,
        encoding: Optional[str] = None,
        mode: Optional[str] = None,
        newline: Optional[str] = None,
        options: Optional[Dict] = None,
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
            sync_mode,
            transformations,
            options,
            partition_by,
            format,
            permission,
            base_path,
        )
        self.host = host
        self.username = username
        self.password = password
        self.file_path = file_path
        self.column_separator = column_separator
        self.has_header = has_header
        self.file_type = file_type
        self.encoding = encoding
        self.mode = mode
        self.newline = newline

    @staticmethod
    def build(context: dict):
        return FileSystemTaskEntity(
            dag_id=context.get("dag_id"),
            dag_class=context.get("dag_class"),
            dag_type=context.get("dag_type"),
            schedule_interval=context.get("schedule_interval"),
            system=context.get("system"),
            country=context.get("country"),
            name=context.get("datasets").get("name"),
            task_owner=context.get("datasets").get("task_owner"),
            owner_team=context.get("datasets").get("owner_team"),
            sync_mode=context.get("datasets").get("sync_mode"),
            transformations=context.get("datasets").get("transformations"),
            notifier=context.get("datasets").get("notifier"),
            options=context.get("datasets").get("options"),
            partition_by=context.get("datasets").get("partition_by"),
            format=context.get("datasets").get("format"),
            permission=context.get("datasets").get("permission"),
            column_separator=context.get("datasets").get("column_separator"),
            file_path=context.get("datasets").get("file_path"),
            has_header=context.get("datasets").get("has_header"),
            host=context.get("host"),
            password=context.get("password"),
            username=context.get("login"),
        )
