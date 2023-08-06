from typing import Optional, Union

from pyiris.infrastructure.common.config import get_key
from pyiris.infrastructure.common.helper import Helper
from pyiris.infrastructure.source.source import Source
from pyiris.infrastructure.source.source_service import SourceService


class FileSystemConfig(object):
    """
    This class intends to get configs to write a file in a file system.

    :param format: the format of file to be written
    :type format: string, required, not null

    :param path: the path where the file will be written
    :type path: string, required, not null

    :param country: the country name to compose the file path
    :type country: string, required, not null

    :param mount_name: an allowed mount name of iris data lake (internal or third's storages)
    :type mount_name: string, required, not null

    :param mode: mode of Spark write
    :type mode: string, required, not null

    :param partition_by: a partition column or list of columns to be guide to the partitioning
    :type partition_by: string or list, optional

    :param options: an allowed spark write option
    :type options: dict, options, not null

    :param base_path: the environment base path
    :type base_path: optional, string
    """

    def __init__(
        self,
        format: str,
        path: str,
        country: str,
        mount_name: str,
        mode: str,
        partition_by: Optional[Union[str, list]] = None,
        options: Optional[dict] = None,
        helper: Optional[Helper] = None,
        base_path: Optional[str] = None,
    ):
        self.format = format
        self.path = path
        self.country = country
        self.mount_name = mount_name
        self.mode = mode
        self.partition_by = partition_by
        self.options = options
        self.full_path = None
        self.source = None
        self.helper = helper or Helper()
        self.base_path = base_path

    @property
    def source(self) -> Source:
        return SourceService.get_by_mount_name(mount_name=self.mount_name)

    @source.setter
    def source(self, value) -> None:
        self._source = value

    @property
    def base_path(self) -> Union[str, None]:
        return self._base_path

    @base_path.setter
    def base_path(self, value) -> None:
        if value is None:
            self._base_path = self.helper.get_base_path()
        else:
            self._base_path = value

    @property
    def full_path(self) -> str:
        if get_key("ENVIRONMENT") == "TEST":
            return "{protocol}{base_path}/{mount_name}/{country}/{path}".format(
                protocol=self.source.protocol,
                base_path=(self.base_path + "/data"),
                mount_name=self.mount_name,
                country=self.country,
                path=self.path,
            )
        else:
            return "{protocol}/{country}/{path}".format(
                protocol=self.source.protocol, country=self.country, path=self.path
            )

    @full_path.setter
    def full_path(self, value) -> None:
        self._full_path = value
