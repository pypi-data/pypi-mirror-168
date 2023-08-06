from typing import List, Union

from pyiris.ingestion.enums.enums import NotifierType


class Notifier(object):
    def __init__(self, type: Union[NotifierType.MS_TEAMS.value], receivers: List[str]):
        self.type = type
        self.receivers = receivers
