from typing import Optional

from pyspark.sql import DataFrame

from pyiris.infrastructure.common.config import get_key
from pyiris.infrastructure.common.exception import FileReaderException, FilterException
from pyiris.infrastructure.common.helper import Helper
from pyiris.infrastructure.service.monitor.log.logger import Logger
from pyiris.infrastructure.spark.spark import Spark
from pyiris.ingestion.extract.readers.reader import Reader
from pyiris.ingestion.validator.file_reader_validator import FileReaderValidator

logger = Logger(__name__)


class FileReader(Reader):
    """
    This class intends to read files in the data lake based on SparkSession.read.
    To read the files the users need to pass some parameters.

    :param table_id: id of the table read. This param may be defined by the user.
    :type table_id: string, required, not null

    :param mount_name: an allowed mount name of iris data lake (internal or third's storages)
    :type mount_name: string, required, not null

    :param country: an allowed country of SAZ
    :type country: string, required, not null

    :param path: a path with at least two hierarchy, in CamelCase, with no special character, except "/"
    :type path: string, required, not null

    :param format: the format of file to be write "avro" or "parquet"
    :type format: string, required, not null

    :param options: a dict with another options to read
    :type options: dict, optional

    :param validator: class FileReaderValidator used to validate with cerberus the arguments passed to read
    :type validator: pyiris.ingestion.validator.file_reader_validator.FileReaderValidator

    :param base_path: the environment base path
    :type base_path: optional, string
    """

    def __init__(
        self,
        table_id: str,
        country: str,
        path: str,
        format: str,
        helper: Optional[Helper] = None,
        mount_name: Optional[str] = None,
        data_lake_zone: Optional[str] = None,
        options: Optional[dict] = None,
        validator: Optional[FileReaderValidator] = None,
        base_path: Optional[str] = None,
    ):
        super().__init__(table_id, helper, base_path)
        self.mount_name = mount_name or data_lake_zone  # TODO remove data_lake_zone
        self.country = country
        self.path = path
        self.full_path = self.get_full_path()
        self.format = format
        self.options = options or None
        self.validator = validator or FileReaderValidator()

    def get_full_path(self) -> str:
        """
        This method is responsible for constructing the full file path according to IRIS mount points.

        :return: a string with the the file path in the IRIS data lake.
        :rtype: string
        """
        if get_key("ENVIRONMENT") == "TEST":
            return "file:///{base_path}/{mount_name}/{country}/{path}".format(
                base_path=self.base_path + "/data",
                mount_name=self.mount_name,
                country=self.country,
                path=self.path,
            )
        else:
            return "/mnt/{mount_name}/{country}/{path}".format(
                mount_name=self.mount_name, country=self.country, path=self.path
            )

    @logger.log_decorator
    def consume(self, spark: Spark, filter: Optional[str] = None) -> DataFrame:
        """
        The consume method is responsible for reading the files in the data lake. The dataframe may be complete or
        filtered.
        The method uses another class pyiris.ingestion.validator.file_reader_validator.FileReaderValidator to
        validate the arguments.
        If the validator do not validate the parameters, an exception with the error value is raised.

        :param spark: a spark object
        :type spark: pyiris.infrastructure.spark.spark.Spark

        :param filter: condition to make a conditional filter
        :type filter: optional, string

        :return: the extracted dataframe
        :rtype: pyspark.sql.dataframe.DataFrame

        :raises: Exception -- Error value
        """
        result = self.validator.consume_validate(file_reader=self.__dict__)
        if result.is_right():
            dataframe = spark.read(
                format=self.format, options=self.options, path=self.full_path
            )
            logger.info("Reading files in the {}".format(self.full_path))
            if filter:
                logger.info(
                    "Reading files with filter in the {}".format(self.full_path)
                )
                return self._filter(dataframe=dataframe, condition=filter)
            else:
                logger.info(
                    "Reading files without filter in the {}".format(self.full_path)
                )
                return dataframe
        else:
            raise FileReaderException(message=result.value(), full_path=self.full_path)

    @logger.log_decorator
    def _filter(self, condition: str, dataframe: DataFrame) -> DataFrame:
        """
        This property method is responsible for getting and execute spark conditional filter over the dataframe.
        It just is executed when param filter is passed in the consume method.

        :param condition: the condition to filter
        :type condition: SQL string condition, not null

        :param dataframe: the dataframe that will be filtered
        :type dataframe: pyspark.sql.dataframe.DataFrame

        :return: the filtered dataframe
        :rtype: pyspark.sql.dataframe.DataFrame

        :raises: FilterException -- Error value
        """
        filter_validator = self.validator.filter_validate(filter={"filter": condition})
        if filter_validator.is_right():
            logger.info("Validating filter condition.")
            return dataframe.filter(condition=condition)
        else:
            logger.error(
                "Error when try to filter dataframe. Invalid parameters: {}".format(
                    filter_validator.value()
                )
            )
            raise FilterException(message=filter_validator.value())
