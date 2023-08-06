import enum
import sys
import time
from datetime import datetime
from functools import wraps

from loguru import logger

from pyiris.infrastructure.thread_local import ThreadLocal


class LogLevel(enum.Enum):
    """Enumerate with Log Levels."""

    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class LogData(object):
    """Log Data object is based on Graylog Extended Log Format (GELF) that is a log format for structured events"""

    def __init__(
        self, message: str, file: str, level: str, _request_id: str, _timestamp: str
    ):
        self.message = message
        self.file = file
        self.level = level
        self._request_id = _request_id
        self._timestamp = _timestamp


class Logger(object):
    """A simple execution logger that's helps to handle with log messages."""

    def __init__(self, module):
        self.module = module
        self.config = {
            "handlers": [
                {"sink": sys.stdout, "format": "{time} | {level} | {message}"},
            ]
        }
        logger.configure(**self.config)
        self.logger = logger

    def info(self, message):
        self._log(self.logger.info, LogLevel.INFO, message)

    def error(self, message):
        self._log(self.logger.error, LogLevel.ERROR, message)

    def debug(self, message):
        self._log(self.logger.debug, LogLevel.DEBUG, message)

    def warn(self, message):
        self._log(self.logger.warning, LogLevel.WARNING, message)

    def log_decorator(self, func):
        """This decorator prints the start, finished and execution time for the decorated function."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            self._log(
                self.logger.debug,
                LogLevel.DEBUG,
                message=f'Start "{func.__name__}" function execution at {datetime.now()}',
            )

            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()

            self._log(
                self.logger.debug,
                LogLevel.DEBUG,
                message=f'Finished executing of "{func.__name__}" function at {datetime.now()}',
            )

            self._log(
                self.logger.debug,
                LogLevel.DEBUG,
                message=f'Method "{func.__name__}" ran in [{round(end - start, 2)}]s',
            )

            return result

        return wrapper

    def _log(self, log_level_function, log_level, message):
        """This prints the log level definition."""
        log_data = LogData(
            _request_id=ThreadLocal.get_request_id(),
            message=message,
            file=self.module,
            level=log_level.value,
            _timestamp=str(datetime.now()),
        )

        log = f"request_id: {log_data._request_id} | file: {self.module} | message: {log_data.message}"
        log_level_function(log)
