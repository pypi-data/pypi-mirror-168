import json
from datetime import date, timedelta
from typing import Dict, Optional

from pyiris.ingestion.task.entity.task_entity import TaskEntity


class RestApiTaskEntity(TaskEntity):
    """
    This class represents the Rest API task entity on source tasks.

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
    :type notifier: pyiris.infrastructure.alert.alert.Alert

    :param url: the base url requested
    :type url: required, string

    :param method: the request method
    :type method: required, string

    :param data_response_mapping: the data location within the response schema as a list
    :type data_response_mapping: required, list

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

    :param options: the Rest API options as a dictionary. Options are body, data_response_mapping, headers and pagination_options
    :type options: Optional, dict

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
        method: str,
        data_response_mapping: list,
        sync_mode: Optional[str] = None,
        transformations: Optional[Dict] = None,
        partition_by: Optional[str] = None,
        format: Optional[str] = None,
        permission: Optional[str] = None,
        options: Optional[Dict] = None,
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
        self.url = url
        self.method = method
        self.data_response_mapping = data_response_mapping
        self.additional_imports = None
        self.pagination_options = None
        self.headers = None

    @property
    def options(self) -> Dict:
        if not self._options:
            return {}
        else:
            body = self._options.get("body")
            if body:
                str_body = json.dumps(body)
                str_body = str_body.replace("today", (date.today()).strftime("%m%d%y"))
                str_body = str_body.replace(
                    "yesterday", (date.today() - timedelta(days=1)).strftime("%m%d%y")
                )
                str_body = str_body.replace(
                    "tomorrow", (date.today() + timedelta(days=1)).strftime("%m%d%y")
                )
                body.update(json.loads(str_body))
            return self._options

    @options.setter
    def options(self, value) -> None:
        self._options = value

    @staticmethod
    def build(context: dict):
        return RestApiTaskEntity(
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
            notifier=context.get("datasets").get("alert"),
            partition_by=context.get("datasets").get("partition_by"),
            format=context.get("datasets").get("format"),
            permission=context.get("datasets").get("permission"),
            options=context.get("datasets").get("options"),
            data_response_mapping=context.get("datasets").get("data_response_mapping"),
            method=context.get("datasets").get("method"),
            url=context.get("datasets").get("url"),
        )
