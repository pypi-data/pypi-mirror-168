import enum


class EnumMeta(enum.EnumMeta):
    def __contains__(cls, item):
        return item in [v.value for v in cls.__members__.values()]


class NotifierType(enum.Enum):
    MS_TEAMS = "ms_teams"


class MetricType(enum.Enum):
    COUNT = "count"
    GAUGE = "gauge"


class TaskExecutionStatus(enum.Enum, metaclass=EnumMeta):
    SUCCESS = 1
    FAILED = 0


class SchedulerFrequency(enum.Enum, metaclass=EnumMeta):
    ONCE = "once"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class IrisMountNames(enum.Enum, metaclass=EnumMeta):
    CONSUMEZONE = "consumezone"
    HISTORYZONE = "historyzone"
    PRELANDINGZONE = "prelandingzone"
    RAWZONE = "rawzone"
    TRUSTEDZONE = "trustedzone"


class ExternalMountNames(enum.Enum, metaclass=EnumMeta):
    ZXVENTURES = "zxventures"
    ZTECH = "ztech"
    BREWDAT = "brewdat"
    ODIN = "bifrost"


class DataLakeMounts(enum.Enum, metaclass=EnumMeta):
    NONPROD = "nonprod"
    PROD = "prod"


class FileFormats(enum.Enum, metaclass=EnumMeta):
    AVRO = "avro"
    PARQUET = "parquet"
    DELTA = "delta"


class Countries(enum.Enum, metaclass=EnumMeta):
    ARGENTINA = "Argentina"
    BOLIVIA = "Bolivia"
    BRAZIL = "Brazil"
    CHILE = "Chile"
    COLOMBIA = "Colombia"
    ECUADOR = "Ecuador"
    GUYANA = "Guyana"
    MEXICO = "Mexico"
    PANAMA = "Panama"
    PARAGUAY = "Paraguay"
    PERU = "Peru"
    SURINAME = "Suriname"
    URUGUAY = "Uruguay"
    VENEZUELA = "Venezuela"
    LAS = "Las"


class SyncModes(enum.Enum, metaclass=EnumMeta):
    OVERWRITE = "overwrite"
    APPEND = "append"
    INCREMENTAL_APPEND = "incremental_append"


class WriterPriority(enum.Enum, metaclass=EnumMeta):
    FILEWRITER = 1
    DWWRITER = 2
    PRESTOWRITER = 3
    RABBITMQWRITER = 4


class PrestoFormat(enum.Enum, metaclass=EnumMeta):
    PARQUET = "parquet"


class IntelligenceModelStages(enum.Enum, metaclass=EnumMeta):
    NONE = "None"
    STAGING = "Staging"
    PRODUCTION = "Production"


class DefaultPartitionColumn(enum.Enum, metaclass=EnumMeta):
    YEAR = "year"
    MONTH = "month"
    DAY = "day"


class Domain(enum.Enum, metaclass=EnumMeta):
    SOURCE = "source"
    ANALYTICAL = "analytical"


class DataLakePermissions(enum.Enum, metaclass=EnumMeta):
    PUBLIC = "public"
    PRIVATE = "private"


class DomainType(enum.Enum, metaclass=EnumMeta):
    SOURCE = "source"
    ANALYTICAL = "analytical"


class DatasetType(enum.Enum, metaclass=EnumMeta):
    TRANSACTIONAL = "transactional"
    DIMENSION = "dimension"
    METRIC = "metric"
    MODEL = "model"


class JdbcDatabaseOptions(enum.Enum, metaclass=EnumMeta):
    SQLSERVER = "sqlserver"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"


class TaskType(enum.Enum, metaclass=EnumMeta):
    JDBC = "jdbc"
    FILESYSTEM = "filesystem"
    RABBITMQ = "rabbitmq"
    RESTAPI = "restapi"
    SHAREPOINT = "sharepoint"
    SERVICEBUS = "servicebus"
