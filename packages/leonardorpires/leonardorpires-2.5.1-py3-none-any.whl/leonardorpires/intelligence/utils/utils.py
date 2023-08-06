"""
These functions are not in production-ready use yet! They have not being tested nor used in any
other classes that we aim to make available at the moment. They are simply here to help
you clarify how can this intelligence sub-package be used and structured.
"""
from typing import Any, Optional, Tuple

import cloudpickle
from pyspark.sql import DataFrame


def split_train_test(
    data, test_size: Optional[float] = 0.1, random_seed: Optional[int] = 42
) -> Tuple[DataFrame, DataFrame]:
    """
    A helper method to split the data into train and test DataFrames.
    By standard it will take
    """
    train, test = data.randomSplit([1 - test_size, test_size], seed=random_seed)
    return train, test


def serialize_object(fitted_model) -> None:
    """
    A helper function to serialize modified objects.
    """
    with open("model_object.pkl") as f:
        cloudpickle.dumps(fitted_model, f)


def serialize_spark_object():
    pass


def deserialize_object(context) -> Any:
    """
    A helper function to deserialize modified objects. The return can be of any kind,
    since every different framework will return a different object.
    """
    with open(context.artifacts["model_object"], "rb") as f:
        loaded_model = cloudpickle.load(f)
    return loaded_model
