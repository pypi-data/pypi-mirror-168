import tempfile
from tempfile import TemporaryDirectory

from pyiris.infrastructure.common.config import environment


class DataLimitationWarning(UserWarning):
    pass


class TemporaryPath(object):
    def __init__(
        self, temporary_path: TemporaryDirectory, name: str, name_without_prefix: str
    ):
        self.temporary_path = temporary_path
        self.name = name
        self.name_without_prefix = name_without_prefix

    def cleanup(self):
        self.temporary_path.cleanup()

    @staticmethod
    def build():
        if environment == "TEST":
            temporary_path = tempfile.TemporaryDirectory()
            path_name = temporary_path.name
            path_name_without_prefix = temporary_path.name
        else:
            temporary_path = tempfile.TemporaryDirectory(dir="/dbfs/FileStore")
            path_name = temporary_path.name
            path_name_without_prefix = temporary_path.name.replace("/dbfs", "")

        return TemporaryPath(
            temporary_path=temporary_path,
            name=path_name,
            name_without_prefix=path_name_without_prefix,
        )
