from typing import Any, Optional

import mlflow
import mlflow.pyfunc
from pyspark.sql import DataFrame
from pyspark.sql.functions import struct

from pyiris.infrastructure import Spark
from pyiris.ingestion.config.file_system_config import FileSystemConfig
from pyiris.ingestion.enums.enums import IntelligenceModelStages
from pyiris.ingestion.extract import FileReader
from pyiris.ingestion.load import FileWriter
from pyiris.intelligence.predict.predict import Predict


class PredictPipeline(Predict):
    """
    This class will define a pipeline for feature engineering + predictions step, for declaring an entire
    Prediction job pipeline. It will firstly lay itself on Databricks dbutils notebook jobs, but later on
    can be extended to local development, as well as other environments

    :param model_name: The name of the registered model on Mlflow's model registry
    :type model_name: str

    :param model_stage: The stage of the model desired to run through this Prediction Pipeline. Accepted: None, Staging or Production
    :type model_stage: str

    :param features_path: The path to the prepared features that will be read for predictions. It is the path argument on
    Pyiris' `:class:FileReader
    :type features_path: str

    :param output_path: The path to the desired output location that will be written with the appended predictions column.
    It is the path argument on Pyiris' `:class:FileSystemConfig for the `:class:FileWriter object
    :type output_path: str

    :param iris_spark: The desired Spark session, defaults to the session from iris' standard Spark object.
    :type iris_spark: ``:class:typing.Any

    :param model_uri: The packaged MLFlow model location. Defaults to the Databricks' models URI
    f"models:/{model_name}/{model_stage}"
    :type model_uri: str

    :param features_country: The country of the Features Dataset that is located on the Datalake. Defaults to `Brazil`
    :type features_country: str

    :param output_country: The country of the Outputs to be written to. Defaults to `Brazil`
    :type output_country: str

    :param partition_column: The column that you wish to partition your predictions to. Defaults to `prediction_date`,
    but you'll have to make sure that is available on your Features dataset
    :type partition_column: str

    :param file_reader: The file reader object. If not passed, will take the Pyiris' `:class:FileReader
    :type file_reader: Any

    :param file_config: The file config object. If not passed, will take the Pyiris' `:class:FileSystemConfig
    :type file_config: Any

    :param file_writer: The file writer object. If not passed, will take the Pyiris' `:class:FileWriter
    :type file_writer: Any
    """

    def __init__(
        self,
        model_name: str = None,
        model_stage: str = None,
        features_path: str = None,
        output_path: str = None,
        iris_spark: Optional[Any] = None,
        model_uri: Optional[str] = None,
        features_country: Optional[str] = "Brazil",
        output_country: Optional[str] = "Brazil",
        partition_column: str = "prediction_date",
        file_reader: Any = None,
        file_config: Any = None,
        file_writer: Any = None,
    ):
        self.iris_spark = iris_spark or Spark()
        self.model_name = model_name
        self.model_stage = model_stage
        self.model_uri = model_uri or f"models:/{self.model_name}/{self.model_stage}"
        self.features_path = features_path
        self.features_country = features_country
        self.output_path = output_path
        self.output_country = output_country
        self.partition_column = partition_column
        self.file_reader = file_reader or FileReader
        self.file_config = file_config or FileSystemConfig
        self.file_writer = file_writer or FileWriter

    def load_model(self, result_type: Optional[Any] = "double"):
        """
        This method will load the model in the desired stage. Accepts
        None, Staging or Production.

        :param result_type: The value can be either a
        ``pyspark.sql.types.DataType`` object or a DDL-formatted type string. Only a primitive
        type or an array ``pyspark.sql.types.ArrayType`` of primitive type are allowed. Check out the supported
        classes on the official mlflow docs: https://www.mlflow.org/docs/latest/_modules/mlflow/pyfunc.html#spark_udf

        :return: A Spark UDF that will apply the model's predict method and returns the ``result_type`` column.
        """
        if self.model_stage not in IntelligenceModelStages:
            raise ValueError(
                "You did not pass a valid model stage! Allowed: None, Staging, Production"
            )

        model_udf = mlflow.pyfunc.spark_udf(
            spark=self.iris_spark.session,
            model_uri=self.model_uri,
            result_type=result_type,
        )

        return model_udf

    def load_features(self) -> DataFrame:
        """
        This function will load the latest Data inputted in the DataLake using the `:class:FileReader from Pyiris
        by default. All of the arguments go in the constructor method.

        :return: The read Spark DataFrame
        :rtype: DataFrame
        """
        reader = self.file_reader(
            table_id="features_table",
            data_lake_zone="consumezone",
            country=self.features_country,
            path=self.features_path,
            format="parquet",
        )

        data = reader.consume(spark=self.iris_spark)

        return data

    @staticmethod
    def predict(
        features: DataFrame, model_udf, prediction_column: Optional[str] = "prediction"
    ) -> DataFrame:
        """
        This method will apply the model UDF with Spark to the features pySpark DataFrame. Under the hood it will
        call the packaged predict method Mlflow implements

        :param features: The features Dataset, that should be read from the Datalake
        :type features: DataFrame

        :param model_udf: The model udf, loaded with the help of Mlflow's pyfunc.spark_udf method.
        :type model_udf: UserDefinedFunction

        :param prediction_column: The name of the prediction column to be added to the feature DataFrame
        :type prediction_column: str

        :return: The features DataFrame with a new column called `prediction`
        :rtype: DataFrame
        """
        udf_inputs = struct(*features.columns)
        new_data = features.withColumn(prediction_column, model_udf(udf_inputs))
        return new_data

    def write_outputs(self, predicted_data: DataFrame) -> None:
        """
        This method will take the DataFrame that has the predictions column and write it to the Datalake
        by using the ``pyiris.ingestion.load.FileWriter.write`` method.

        :param predicted_data: The DataFrame with the predictions column added to it.
        :type predicted_data: DataFrame
        """
        file_config = self.file_config(
            mount_name="consumezone",
            country=self.output_country,
            path=self.output_path,
            mode="overwrite",
            partition_by=self.partition_column,
            format="parquet",
        )

        self.file_writer(config=file_config).write(dataframe=predicted_data)

    def run(self):
        """
        This method will chain together the sequence of operations for making the predictions and writing them
        to the consumezone in our Datalake.
        """
        features = self.load_features()
        model_udf = self.load_model()
        output_dataframe = self.predict(features, model_udf)
        self.write_outputs(output_dataframe)
