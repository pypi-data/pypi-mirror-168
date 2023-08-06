from io import StringIO
from typing import Optional

from pyiris.infrastructure.common.exception import CSVFileException
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.smb.smb_connection import SMBConnection
from pyiris.ingestion.extract.readers.reader import Reader

logger = Logger(__name__)


class FileSystemReader(Reader):
    """
    This class will connect to an SMB database, get a file and return it as a DataFrame.
    It inherits from the :class:pyiris.ingestion.extract.readers.reader.Reader and also implements
    the same method, with its signature.

    :param file_name: The name of the desired file to be read
    :type file_name: str

    :param file_path: The path where the file is at.
    :type file_path: str

    :param connection_engine: The connection engine to be used. Defaults to the SMBConnection object.
    :type connection_engine: Optional, SMBConnection

    :param file_type: What is the file format. Defaults to CSV
    :type file_type: str

    :param encoding: If the user desires to read the file with some encoding. Defaults to utf-8
    :type encoding: Optional, str

    :param mode: How to actually read the file. Defaults to "r" as in "read". The user might also choose
    to read as a binary, for example, with "rb". Should mostly be changed when working with text files
    :type mode: Optional, str

    :param newline: How to identify a line break. Defaults to "\n"
    :type newline: Optional, str

    """

    def __init__(
        self,
        file_name: str,
        file_path: str,
        connection_engine: SMBConnection,
        file_type: Optional[str] = None,
        encoding: Optional[str] = None,
        mode: Optional[str] = None,
        newline: Optional[str] = None,
    ):
        super().__init__(table_id=file_name)
        self.file_name = file_name
        self.file_path = file_path
        self.connection_engine = connection_engine
        self.file_type = file_type or "csv"
        self.encoding = encoding or "utf-8"
        self.mode = mode or "r"
        self.newline = newline or "\n"

    @logger.log_decorator
    def consume(self, **kwargs) -> StringIO:
        """
        This method will consume the file from the File System and return it as a StringIO object.

        :param kwargs: Arguments.
        :type kwargs: Dict
        """

        if self.file_type in ["csv"]:
            logger.info("Reading [CSV] file.")
            return self.connection_engine.get_file(
                path=self.file_path,
                file_name=self.file_name,
                file_type=self.file_type,
                encoding=self.encoding,
                mode=self.mode,
                newline=self.newline,
            )

        else:
            message = (
                "File type not supported. You can only read CSV files at this moment!"
            )
            raise CSVFileException(message=message)
