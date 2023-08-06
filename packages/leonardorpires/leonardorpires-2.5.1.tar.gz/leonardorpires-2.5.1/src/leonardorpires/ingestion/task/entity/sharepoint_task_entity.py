from typing import Dict, Optional

from pyiris.ingestion.task.entity.task_entity import TaskEntity


class SharepointTaskEntity(TaskEntity):
    """
    This class represents the Sharepoint task entity on source tasks.

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

    :param url: the url for the Sharepoint connection
    :type url: string

    :param client_id: the client id for the Sharepoint connection
    :type client_id: string

    :param client_secret: the client secret for the Sharepoint connection
    :type client_secret: string

    :param file_format: the file format
    :type file_format: string

    :param file_folder: the file folder
    :type file_folder: string

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
        url: str,
        client_id: str,
        client_secret: str,
        file_format: str,
        file_folder: str,
        sync_mode: Optional[str] = None,
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
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.file_format = file_format
        self.file_folder = file_folder

    @staticmethod
    def build(context: dict):
        return SharepointTaskEntity(
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
            client_id=context.get("login"),
            client_secret=context.get("password"),
            file_folder=context.get("datasets").get("file_folder"),
            file_format=context.get("datasets").get("file_format"),
            url=context.get("host"),
        )
