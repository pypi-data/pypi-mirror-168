from typing import Optional

from pyiris.infrastructure.common.message import ErrorMessage
from pyiris.infrastructure.integration.ms_teams.ms_teams import MsTeams
from pyiris.infrastructure.service.metadata.entity.metadata_entity import MetadataEntity
from pyiris.ingestion.enums.enums import NotifierType
from pyiris.ingestion.task.entity.task_entity import TaskEntity


class NotifierService(object):
    def __init__(
        self,
        task_entity: TaskEntity,
        metadata_entity: MetadataEntity,
        ms_teams: Optional[MsTeams] = None,
    ):
        self.task_entity = task_entity
        self.metadata_entity = metadata_entity
        self.ms_teams = ms_teams or MsTeams()

    def on_error(self, error_message, traceback):
        if self.task_entity.notifier.type == NotifierType.MS_TEAMS.value:
            error_message = ErrorMessage.build(
                task_name=self.task_entity.name,
                message=error_message,
                traceback=traceback,
            )

            for receiver in self.task_entity.notifier.receivers:
                self.ms_teams.send_error_message(
                    webhook_url=receiver, message=error_message
                )
