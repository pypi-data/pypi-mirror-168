from urllib.parse import urlparse

from office365.sharepoint.client_context import ClientContext

from pyiris.infrastructure.common.exception import SharepointReaderException
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.extract.readers.reader import Reader

logger = Logger(__name__)


class SharePointReader(Reader):
    """
    This class intends to download a file from a SharePoint Site folder and store into a directory.
    To read the messages the users need to pass some parameters.

    :param file_name: a SharePoint file name.
    :type file_name: string, required, not null

    :param file_folder: a SharePoint file folder.
    :type file_folder: string, required, not null

    :param file_format: a file format e.g csv, xlsx or xls.
    :type file_format: string, required, not null

    :param engine: an engine to execute the download
    :type engine: ClientContext (default), optional
    """

    def __init__(
        self, file_name: str, file_folder: str, file_format: str, engine: ClientContext
    ):
        super().__init__(table_id=file_name)
        self.file_name = file_name
        self.file_folder = file_folder
        self.file_format = file_format
        self.engine = engine

    @logger.log_decorator
    def consume(self, **kwargs):
        """This method intends to handle how download the file from a specific SharePoint Site folder,
        build the temporary path and remote url and then save file into directory.

        :param kwargs: Arguments.
        :type kwargs: Dict

        :return: a list of message.
        :rtype: List[dict]
        """
        if not kwargs.get("temporary_path"):
            raise SharepointReaderException(
                message="Missing parameter temporary_path is required!"
            )

        path = f"{kwargs.get('temporary_path')}/{self.file_name}.{self.file_format}"
        remote_url = f"{urlparse(self.engine.base_url).path}/{self.file_folder}/{self.file_name}.{self.file_format}"
        with open(path, "wb") as local_file:
            self.engine.web.get_file_by_server_relative_url(remote_url).download(
                local_file
            ).execute_query()

        logger.info(
            f"File downloaded successfully from SharePoint Site folder: {path}, remote url: {remote_url}"
        )
