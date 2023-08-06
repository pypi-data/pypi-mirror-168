from pyiris.ingestion.enums.enums import MetricType


class Tag(object):
    def __init__(
        self,
        task_name: str = None,
        task_owner: str = None,
        owner_team: str = None,
        data_owner: str = None,
        source_system: str = None,
        country: str = None,
    ):

        self.task_name = task_name
        self.task_owner = task_owner
        self.owner_team = owner_team
        self.data_owner = data_owner
        self.source_system = source_system
        self.country = country


class Metric(object):
    def __init__(self, name: str, value: int, metric_type: MetricType, tag: Tag):
        self.name = name
        self.value = value
        self.metric_type = metric_type
        self.tag = tag
