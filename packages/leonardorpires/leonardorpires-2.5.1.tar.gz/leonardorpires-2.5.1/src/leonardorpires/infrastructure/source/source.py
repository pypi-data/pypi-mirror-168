import os
from typing import Optional, Union

from pyiris.infrastructure.common.config import get_key
from pyiris.infrastructure.spark.spark import SparkExtraConfigs
from pyiris.ingestion.enums.enums import IrisMountNames


class Source(object):
    def __init__(self, mount_name: str, protocol: Optional[str] = None):
        self.mount_name = mount_name
        self.protocol = protocol

    def build(self):
        pass


class Iris(Source):
    """
    This class is responsible for checking the Iris source rules.

    :param mount_name: the given mount_name that will be checked
    :type mount_name: String

    :param engine_extra_configs: spark session that will set the extra configs
    :type engine_extra_configs: optional, :class:pyiris.infrastructure.spark.spark.SparkExtraConfigs

    :param protocol: the complete protocol/endpoint
    :type protocol: string
    """

    def __init__(
        self,
        mount_name: str,
        engine_extra_configs: Optional[SparkExtraConfigs] = None,
        protocol: str = None,
    ):

        super().__init__(mount_name, protocol)
        self.engine_extra_configs = engine_extra_configs or SparkExtraConfigs()

    def build(self) -> Source:
        """
        This method checks if the mount_name argument is "rawzone", or "trusted_zone", or "prelandingzone", or "historyzone" or "consumezone". If True,
        return the Iris abfs endpoint and set the correspondents spark extra configs. Else, call the next class to
        check the correspondent rule.

        :return: the source object
        :rtype: pyiris.infrastructure.source.source.Iris

        :raises: ValueError -- "Mount name not allowed"
        """
        if self.mount_name in IrisMountNames:
            if get_key("ENVIRONMENT") == "TEST":
                self.protocol = "file:///"
            else:
                self.engine_extra_configs.set_spark_abfs_iris()
                self.protocol = "abfss://{mount_name}@{lakeAccountName}.dfs.core.windows.net".format(
                    mount_name=self.mount_name,
                    lakeAccountName=get_key("lakeAccountName"),
                )

            return self
        else:
            raise ValueError("Mount name not allowed")


class Bifrost(Source):
    """
    This class is responsible for checking the Bifrost source rules.

    :param mount_name: the given mount_name that will be checked
    :type mount_name: String

    :param engine_extra_configs: spark session that will set the extra configs
    :type engine_extra_configs: optional, :class:pyiris.infrastructure.spark.spark.SparkExtraConfigs

    :param next_class: the next rule class that will be called
    :type next_class: pyiris.infrastructure.source.source.Source
    """

    def __init__(
        self,
        mount_name: str,
        next_class: Source,
        engine_extra_configs: Optional[SparkExtraConfigs] = None,
        protocol: str = None,
    ):

        super().__init__(mount_name, protocol)
        self.next_class = next_class
        self.engine_extra_configs = engine_extra_configs or SparkExtraConfigs()

    def build(self) -> Union[None, Source]:
        """
        This method checks if the mount_name argument is "bifrost". If True, return the bifrost endpoint and set the
        correspondents spark extra configs. Else, call the next class to check the correspondent rule.

        :return: a string with the bifrost wasbs protocol or call the net check class
        :rtype: Union[str, :class:pyiris.infrastructure.source.source.Source]
        """
        if self.mount_name == "bifrost":
            self.engine_extra_configs.set_spark_wasbs_bifrost()
            self.protocol = "wasbs://{BifrostContainer}@{BifrostBlobAccountName}.blob.core.windows.net".format(
                BifrostContainer=get_key("BifrostContainer"),
                BifrostBlobAccountName=get_key("BifrostBlobAccountName"),
            )
            return self
        else:
            return self.next_class.build()


class Brewdat(Source):
    """
    This class is responsible for checking the Brewdat source rules.

    :param mount_name: the given mount_name that will be checked
    :type mount_name: String

    :param engine_extra_configs: spark session that will set the extra configs
    :type engine_extra_configs: optional, :class:pyiris.infrastructure.spark.spark.SparkExtraConfigs

    :param protocol: the complete protocol/endpoint
    :type protocol: string

    :param next_class: the next rule class that will be called
    :type next_class: pyiris.infrastructure.source.source.Source
    """

    def __init__(
        self,
        mount_name: str,
        next_class: Source,
        engine_extra_configs: Optional[SparkExtraConfigs] = None,
        protocol: str = None,
    ):

        super().__init__(mount_name, protocol)
        self.next_class = next_class
        self.engine_extra_configs = engine_extra_configs or SparkExtraConfigs()

    def build(self) -> Source:
        """
        This method checks if the mount_name argument is "brewdat". If True, return the Brewdat abfss endpoint and set
        the correspondent spark extra configs. Else, call the next class to check the correspondent rule.


        :return: the source object
        :rtype: pyiris.infrastructure.source.source.Iris

        :raises: ValueError -- "Mount name not allowed"
        """
        if self.mount_name == "brewdat":
            if os.environ.get("ENVIRONMENT") == "prod":
                self.engine_extra_configs.set_spark_abfs_brewdat()
                self.protocol = "abfss://iris-plz@{IrisBrewdatAccountName}.dfs.core.windows.net".format(
                    IrisBrewdatAccountName=get_key("IrisBrewdatAccountName"),
                )
            else:
                self.engine_extra_configs.set_spark_wasbs_analyticsplatformblob()
                self.protocol = (
                    "wasbs://brewdat@{blobAccountName}.blob.core.windows.net".format(
                        blobAccountName=get_key("blobAccountName"),
                    )
                )
            return self
        else:
            return self.next_class.build()
