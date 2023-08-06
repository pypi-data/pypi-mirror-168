from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

from pyiris.infrastructure.common.config import get_key

_database_url = "postgresql://{}:{}@{}:{}/{}".format(
    get_key("IrisPostgresUser"),
    get_key("IrisPostgresPassword"),
    get_key("IrisPostgresHost"),
    get_key("IrisPostgresPort"),
    get_key("IrisPostgresDatabaseName"),
)
_engine = create_engine(
    _database_url, poolclass=NullPool, connect_args={"connect_timeout": 5}
)
_factory = sessionmaker(bind=_engine, autoflush=False)
Session = scoped_session(sessionmaker(bind=_engine))
