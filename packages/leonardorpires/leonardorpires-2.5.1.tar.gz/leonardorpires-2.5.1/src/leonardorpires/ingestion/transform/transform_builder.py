from pyiris.infrastructure.common.exception import TansformBuilderException
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.ingestion.enums.enums import IrisMountNames
from pyiris.ingestion.transform import HashTransformation
from pyiris.ingestion.transform.transformations.custom.custom import (
    add_ingestion_date,
    drop_duplicate,
    snakecase_column_names,
)
from pyiris.ingestion.transform.transformations.custom_transformation import (
    CustomTransformation,
)

logger = Logger(__name__)


class SourceTransformBuilder(object):
    """
    This class intends to build the transformations for src.pyiris.ingestion.task.source_tasks.source_task.SourceTask
    class.
    """

    def __init__(self):
        self.transformations = []

    @staticmethod
    @logger.log_decorator
    def build(context: dict, zone: str):
        try:
            context = context.get("transformations", {})
            source_transform_builder = SourceTransformBuilder()
            source_transform_builder._set_default_transformations(
                zone=zone, context=context
            )
            source_transform_builder._set_custom_transformations(
                zone=zone, context=context
            )
        except Exception as e:
            raise TansformBuilderException(message=e)

        logger.info(f"Successfully built transformations to {zone}")
        return source_transform_builder

    def _set_default_transformations(self, zone: str, context: dict) -> None:
        """
        This method intends to set the default transformations for rawzone and trustedzone. The transformations are:

        Rawzone:
            pyiris.ingestion.transform.transformations.custom.custom.snakecase_column_names
            pyiris.ingestion.transform.transformations.custom.custom.add_ingestion_date

        Trustedzone:
            pyiris.ingestion.transform.transformations.custom.custom.drop_duplicate

        PS: the drop_duplicate transformation is default, but the 'exclude_only' and 'based_on_columns' may be passed for
        changing the way the dro_duplicate is made, considering different columns on the process. If nothing is passed,
        the drop will consider all the dataset columns.


        :param zone: the data lake zone
        :zone type: string

        :param context: the transformations context
        :context type: dict
        """
        if zone == IrisMountNames.RAWZONE.value:
            self.transformations.extend(
                [
                    CustomTransformation(
                        name="snake case column names",
                        description="snake case all dataframe column names",
                        method=snakecase_column_names,
                    ),
                    CustomTransformation(
                        name="add ingestion date",
                        description="add control ingestion date columns",
                        method=add_ingestion_date,
                    ),
                ]
            )
        elif zone == IrisMountNames.TRUSTEDZONE.value:
            drop_options = context.get("drop_duplicate")

            exclude_only = (
                drop_options.get("exclude_only")
                if drop_options and drop_options.get("exclude_only")
                else None
            )
            based_on_columns = (
                drop_options.get("based_on_columns")
                if drop_options and drop_options.get("based_on_columns")
                else None
            )

            self.transformations.append(
                CustomTransformation(
                    name="drop duplicate",
                    description="apply drop duplicate transformation on all dataframe rows",
                    exclude_only=exclude_only,
                    based_on_columns=based_on_columns,
                    method=drop_duplicate,
                )
            )

    def _set_custom_transformations(self, context: dict, zone: str) -> None:
        """
        This method intends to set all optional transformations on source module. Nowadays the available transformations
        are:
            pyiris.ingestion.transform.HashTransformation

        :param context: the optional transformations context
        :type context: dict
        """
        self._set_hash_transformation(zone=zone, context=context)

    def _set_hash_transformation(self, context: dict, zone: str) -> None:
        """
        This method intends to set the hash transformations if zone = 'trustedzone' and 'hash' is in the context.
        In the context parameter, the hash has to be passed, with this way: {'hash': {'from_columns': ['columns']}}.

        :param zone: the data lake zone
        :zone type: string

        :param context: the transformations context
        :context type: dict
        """
        if zone == IrisMountNames.TRUSTEDZONE.value and context.get("hash"):
            hash_context = context.get("hash")
            self.transformations.append(
                HashTransformation(
                    name="hash columns",
                    description="apply hash transformation on dataframe columns",
                    from_columns=hash_context.get("from_columns"),
                )
            )
