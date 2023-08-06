from pyiris.infrastructure.source.source import Bifrost, Brewdat, Iris, Source


class SourceService(object):
    """
    This class intends to concatenate the rule classes, based on "Chain of responsibility" design pattern, to get the
    correspondent source endpoint and set the correspondent extra spark extra configs.
    """

    @staticmethod
    def get_by_mount_name(mount_name: str) -> Source:
        """
        This method intends to call all check classes to check if some rules match with the inputted argument. If there
        is some rule match, an endpoint is returned and the correspondent spark extra configs are configured.

        :param mount_name: the mount name that will be checked
        :type mount_name: String

        :return: the concatenated check classes calls
        :rtype: :class:pyiris.ingestion.config.configs_setter.file_system_config_setter.BifrostConfig
        """
        return Brewdat(
            mount_name=mount_name,
            next_class=Bifrost(
                mount_name=mount_name, next_class=Iris(mount_name=mount_name)
            ),
        ).build()
