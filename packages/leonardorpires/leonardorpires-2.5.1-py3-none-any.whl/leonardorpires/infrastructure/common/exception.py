from datetime import datetime

from pyiris.infrastructure.service.monitor.log.logger import Logger

logger = Logger(__name__)


class PyIrisConnectionException(Exception):
    """Exception raised for errors in the Connection Readers"""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(message)
        return message


class PyIrisTaskException(Exception):
    """Exception raised for errors in the Ingestion Tasks"""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(message)
        return message


class FilterException(Exception):
    """Exception raised for errors in the Filter File Reader"""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(message)
        return message


class RabbitMQTaskExecutionTimeoutException(Exception):
    """Exception raised when RabbitMQ consumer reached execution timeout"""

    def __str__(self):
        message = f"Reached execution timeout at {datetime.now()}"
        logger.error(message)
        return message


class RabbitMQTaskNoMessagesFoundException(Exception):
    """Exception raised when RabbitMQ consumer not found any message in queue"""

    def __str__(self):
        message = "No messages found in the queue"
        logger.error(message)
        return message


class RabbitMQTaskInactivityTimeout(Exception):
    """Exception raised when RabbitMQ consumer reached inactivity timeout"""

    def __str__(self):
        message = f"Reached inactivity timeout at {datetime.now()}"
        logger.error(message)
        return message


class SharePointTaskCouldNotReadFileException(Exception):
    """Exception raised when SharePoint Task could not read file"""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(message)
        return message


class HashTransformationException(Exception):
    """Exception raised when Invalid Spark Type."""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(message)
        return message


class SparkTransformationException(Exception):
    """Exception raised when Failed to transform on the dataframe that is injected into it."""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Failed to transform on the dataframe that is injected into it. Message: {repr(self.message)}"
        logger.error(message)
        return message


class TansformBuilderException(Exception):
    """Exception raised when Invalid Spark Type."""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Error on building the transformations for the source module. Message: {repr(self.message)}"
        logger.error(message)
        return message


class FileWriterValidatorException(Exception):
    """Exception raised when the FileWriterValidator do not validate the parameters"""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(message)
        return message


class PrestoWriterValidatorException(Exception):
    """Exception raised when Presto Writer validator doesn't work validate the parameters"""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(message)
        return message


class SqlWriterValidatorException(Exception):
    """Exception raised when Sql Writer validator doesn't validate the parameters"""

    def __str__(self):
        message = "There was an error saving with SqlWriter"
        logger.error(message)
        return message


class FileReaderException(Exception):
    """Exception raised when occurs error validating filter condition."""

    def __init__(self, message: str, full_path: str):
        super(Exception, self).__init__(message)
        self.message = message
        self.full_path = full_path

    def __str__(self):
        message = f"Error when try to read path: {self.full_path}. Invalid parameters: {self.message})"
        logger.error(message)
        return message


class CSVFileException(Exception):
    """Exception raised when file type is not supported."""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(message)
        return message


class JdbcReaderException(Exception):
    """Exception raised when occurs error to reading data from JDBC."""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(message)
        return message


class SharepointReaderException(Exception):
    """Exception raised when SharePoint parameters are not valid."""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(message)
        return message


class ReaderOptionsDatabaseException(Exception):
    """Exception raised when Database Type parameters are not supported."""

    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(message)
        return message


class DataDogFailedSendMetricsException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message

    def __str__(self):
        message = f"Message: {repr(self.message)}"
        logger.error(
            "Error when try to send metrics to DataDog. {message}".format(
                message=message
            )
        )
