from typing import Optional

from pyiris.infrastructure import Spark
from pyiris.ingestion.extract import ExtractService
from pyiris.ingestion.load import LoadService
from pyiris.ingestion.transform import TransformService


class Task(object):
    """
    This object intends to execute the extract, transform and load services.
    :param extract_service: the extract service object, listing readers
    :type extract_service: pyiris.ingestion.extract.ExtractService
    :param load_service: the load service object, listing writers
    :type load_service: pyiris.ingestion.load.LoadService
    :param transform_service: the transform service object, listing transformations
    :type transform_service: pyiris.ingestion.transform.TransformService, optional
    """

    def __init__(
        self,
        extract_service: ExtractService,
        load_service: LoadService,
        transform_service: Optional[TransformService] = None,
    ) -> None:
        super().__init__()
        self.extract_service = extract_service
        self.transform_service = transform_service
        self.load_service = load_service

    def run(self, spark: Spark):
        """This function intends to execute sequentially:
        -the ExtractService handler, resulting to an extracted dataframe,
        -optionally, the TransformService handler, resulting to a transformed dataframe
        -the LoadService commit.
        :param spark: the Spark session used to extract the dataset
        :type spark: optional, pyspark.sql.session.SparkSession
        """
        extracted_dataframe = self.extract_service.handler(spark=spark)
        if self.transform_service:
            transformed_dataframe = self.transform_service.handler(
                dataframe=extracted_dataframe
            )
        else:
            transformed_dataframe = extracted_dataframe
        self.load_service.commit(dataframe=transformed_dataframe)
