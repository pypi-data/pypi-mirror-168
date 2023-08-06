from abc import abstractmethod
from typing import Dict, Optional, Union

from pyiris.infrastructure.common.helper import Helper
from pyiris.infrastructure.service.monitor.notifier.notifier import Notifier
from pyiris.ingestion.enums.enums import (
    DataLakePermissions,
    DefaultPartitionColumn,
    FileFormats,
    SyncModes,
)


class TaskEntity(object):
    """
    This class represents the task entity on source tasks.

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

    :param sync_mode: the write mode to save files in the rawzone, allowed overwrite and append
    :type sync_mode: string, optional.

    :param nofity: the alert definitions
    :type nofity: pyiris.infrastructure.alert.alert.Alert

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
        options: Optional[Dict] = None,
        sync_mode: Optional[str] = None,
        transformations: Optional[Dict] = None,
        partition_by: Optional[str] = None,
        format: Optional[str] = None,
        permission: Optional[str] = None,
        base_path: Optional[str] = None,
    ):

        self.dag_id = dag_id
        self.dag_class = dag_class
        self.dag_type = dag_type
        self.schedule_interval = schedule_interval
        self.system = system
        self.country = country
        self.name = name
        self.task_owner = task_owner
        self.owner_team = owner_team
        self.base_path = base_path
        self.transformations = transformations
        self.partition_by = partition_by
        self.notifier = notifier
        self.sync_mode = sync_mode
        self.format = format or FileFormats.DELTA.value
        self.permission = permission or DataLakePermissions.PUBLIC.value
        self.options = options or {}
        self.path = None

    @property
    def name(self) -> str:
        return Helper.snake_case(string=self._name)

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @property
    def path(self) -> str:
        return f"{Helper.camel_case(string=self.system)}/{Helper.camel_case(string=self.name)}"

    @path.setter
    def path(self, value) -> None:
        self._path = value

    @property
    def notifier(self) -> Notifier:
        return Notifier(
            type=self._notifier.get("type"), receivers=self._notifier.get("receivers")
        )

    @notifier.setter
    def notifier(self, value) -> None:
        self._notifier = value

    @property
    def partition_by(self) -> Union[str, list]:
        if self._partition_by is not None:
            return Helper.snake_case(self._partition_by)
        else:
            return [
                DefaultPartitionColumn.YEAR.value,
                DefaultPartitionColumn.MONTH.value,
                DefaultPartitionColumn.DAY.value,
            ]

    @partition_by.setter
    def partition_by(self, value) -> None:
        self._partition_by = value

    @property
    def transformations(self) -> dict:
        default_drop_duplicate = {
            "drop_duplicate": {"exclude_only": ["year", "month", "day"]}
        }

        if self._transformations:
            if not self._transformations.get("drop_duplicate"):
                self._transformations.update(default_drop_duplicate)
        else:
            self._transformations = {}
            self._transformations.update(default_drop_duplicate)

        return self._transformations

    @transformations.setter
    def transformations(self, value) -> None:
        self._transformations = value

    @property
    def sync_mode(self) -> str:
        if not self._sync_mode:
            return SyncModes.APPEND.value
        elif self._sync_mode == SyncModes.INCREMENTAL_APPEND.value:
            self.options.update({"mergeSchema": "True"})
            return SyncModes.APPEND.value
        elif self._sync_mode == SyncModes.OVERWRITE.value:
            self.options.update({"overwriteSchema": "True"})
            return SyncModes.OVERWRITE.value
        else:
            return SyncModes.APPEND.value

    @sync_mode.setter
    def sync_mode(self, value) -> None:
        self._sync_mode = value

    @staticmethod
    @abstractmethod
    def build(context: dict):
        pass
