from io import StringIO

from smbclient import open_file


class SMBConnection(object):
    """
    This class is used to make a connection to a remote File System using the SMB Protocol.
    It relies on the smbprotocol Python library, which can be found at the PyPI repository.
    If you want to read more about it, please visit: https://github.com/jborean93/smbprotocol

    :param username: The username to be used when mounting the connection
    :type username: str

    :param password: The password to authenticate to the remote server
    :type password: str

    :param host: The SMB server endpoint
    :type host: str
    """

    def __init__(self, username: str, password: str, host: str):
        self.username = username
        self.password = password
        self.host = host

    def get_file(
        self,
        path: str,
        file_name: str,
        file_type: str,
        encoding: str,
        mode: str,
        newline: str,
    ) -> StringIO:
        """
        This method will use the built-in open_file method in the smbprotocol library to
        read a file from the SMB server and return it as a StringIO object. With that, it will be
        possible to "parse" it to the desired data type (such as a pyspark DataFrame).

        :param path: The path where the file resides
        :type path: str

        :param file_name: The name of the desired file.
        :type file_name: str

        :param file_type: What is the file format. Defaults to CSV
        :type file_type: Optional, str

        :param encoding: If the user desires to read the file with some encoding. Defaults to utf-8
        :type encoding: Optional, str

        :param mode: How to actually read the file. Defaults to "r" as in "read". The user might also choose
        to read as a binary, for example, with "rb". Should mostly be changed when working with text files
        :type mode: Optional, str

        :param newline: How to identify a line break. Defaults to "\n"
        :type newline: Optional, str


        :return: The in-memory StringIO object containing the read file.
        :rtype: StringIO

        """

        with open_file(
            path=self._build_path_string(
                path=path, file_name=file_name, file_type=file_type
            ),
            username=self.username,
            password=self.password,
            encoding=encoding,
            mode=mode,
            newline=newline,
        ) as file:
            text_file = StringIO(file.read())

        return text_file

    def _build_path_string(
        self, path: str, file_name: str, file_type: str = "csv"
    ) -> str:
        """
        This is a helper method to build the entire path string, given a path, the filename and its
        type.

        :param path: The path where the file resides
        :type path: str

        :param file_name: The name of the desired file.
        :type file_name: str

        :param file_type: What is the file format. Defaults to CSV
        :type file_type: str

        :return: The complete path to be used by the get_file method
        :rtype: str
        """
        return rf"\\{self.host}\{path}\{file_name}.{file_type}"
