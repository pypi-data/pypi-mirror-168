from abc import ABCMeta
from typing import Any, Optional

from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import DataFrame

from pyiris.infrastructure import Spark
from pyiris.ingestion.extract import FileReader
from pyiris.intelligence.models import BaseIrisModel
from pyiris.intelligence.utils.utils import deserialize_object, serialize_spark_object


class SparkMLWrapper(BaseIrisModel, metaclass=ABCMeta):
    """
    ! Class not yet implemented !
    This class intends to simplify the way our Data Scientists will have to handle Pyspark to train their models.
    Our aim is to have something as similar as possible to what is implemented in the Scikit-learn base estimator.
    We also want to make it easier to extend its usage to whatever needs the users feel are necessary for their own
    implementations.

    Basic usage:

    ```python
    rf_classifier = RandomForestClassifier(numTrees=10, featuresCol='features', labelCol='TARGET')

    model_wrapper = SparkMLWrapper(
        model = rf_classifier,
        training_data_path = 'Test/IntelligenceDatasets/Iris',
        country = 'Brazil'
    )

    features_list = ["col1", "col2"]

    model_wrapper.fit(features_list)

    model_wrapper.predict(data)
    ```
    """

    def __init__(
        self, training_data_path: str, model: Any, country: str, iris_spark: Optional
    ):
        super().__init__(model=model)
        self.training_data_path = training_data_path
        self.iris_spark = iris_spark or Spark()
        self.country = country or "Brazil"

    def load_context(self, context) -> None:
        self.model = deserialize_object(context)

    def load_training_data(self):
        training_data = FileReader(
            table_id="train_data",
            mount_name="consumezone",
            country=self.country,
            format="parquet",
            path=self.training_data_path,
        ).consume(spark=self.iris_spark)
        return training_data

    def fit(self, features_list, output_col: Optional[str] = "features"):
        training_data = self.load_training_data()
        assembler = VectorAssembler(inputCols=features_list, outputCol=output_col)
        pipeline = Pipeline(stages=[assembler, self.model])
        fitted_model = pipeline.fit(training_data)
        serialize_spark_object(fitted_model)

    def predict(self, context, data):
        return self.model.predict(data)

    @staticmethod
    def define_features_column(
        training_data: DataFrame,
        features_list: list,
        output_col: Optional[str] = "features",
    ):
        assembler = VectorAssembler(inputCols=features_list, outputCol=output_col)
        featurized_dataset = assembler.transform(training_data)
        return featurized_dataset

    # TODO implement validation method to be reused
    def validate(self, training_data):
        pass

    # TODO implement get signature method (model's i/o format)
    def get_signature(self, **kwargs):
        pass
