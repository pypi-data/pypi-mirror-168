import os
from datetime import datetime
from typing import Dict, List, Optional, Union

from pyiris.infrastructure.integration import Git, MlFlow
from pyiris.infrastructure.service.metadata.entity.model_entity import Model
from pyiris.infrastructure.service.metadata.entity.model_version_entity import (
    ModelVersion,
)


class ModelMapper(object):
    """
    This class intends to map the metadata about machine learning models to a declarative base sqlalchemy object
    representing 'model' table.
    """

    def __init__(self, git: Optional[Git] = None, mlflow: Optional[MlFlow] = None):
        self.git = git or Git()
        self.mlflow = mlflow or MlFlow()

    def to_entities(
        self,
        model_definition: Dict,
        product_definition: Dict,
        project_metadata: List,
        model_definition_path: str,
    ) -> Union[List, None]:
        models = list()
        models_definition = model_definition.get("models")
        if not models_definition:
            return None

        for model_definition in models_definition:
            model_name = model_definition.get("name")
            model_version = ModelMapper.get_model_version(
                model_definition=model_definition
            )

            models.append(
                Model(
                    name=model_name,
                    deployment_flavor=ModelMapper.get_deployment_flavor(
                        product_definition=product_definition
                    ),
                    repository=ModelMapper.get_repository(),
                    description=ModelMapper.get_model_description(
                        model_definition=model_definition
                    ),
                    project_docs_url=ModelMapper.get_documentation_link(),
                    versions=self.to_model_version_entity(
                        model_name=model_name,
                        model_version=model_version,
                        project_metadata=project_metadata,
                        model_definition_path=model_definition_path,
                    ),
                )
            )

        return models

    def to_model_version_entity(
        self,
        model_name: str,
        model_version: int,
        project_metadata: List[Dict],
        model_definition_path: str,
    ) -> Union[List[ModelVersion], None]:
        versions = list()
        model_registry = ModelMapper.get_mlflow_registry(
            model_name=model_name, model_version=model_version
        )
        model_success_metric = ModelMapper.get_model_success_metric(
            project_metadata=project_metadata
        )
        model_metric_value = ModelMapper.get_model_metric_value(
            project_metadata=project_metadata
        )
        model_last_commit = self.git.get_last_commit_of_a_file(
            file_path=model_definition_path
        )
        model_artifact = self.mlflow.get_model_artifact(
            model_name=model_name, model_version=model_version
        )
        model_created_date = ModelMapper.get_model_created_date(
            model_artifact=model_artifact, model_name=model_name
        )

        versions.append(
            ModelVersion(
                version=model_version,
                mlflow_registry=model_registry,
                commit_hash=model_last_commit,
                success_metric=model_success_metric,
                metric_value=model_metric_value,
                model_input=model_artifact[model_name]["signature"]["inputs"],
                model_output=model_artifact[model_name]["signature"]["outputs"],
                mlflow_created_date=model_created_date,
            )
        )

        return versions

    @staticmethod
    def get_deployment_flavor(product_definition: dict) -> str:
        deployment_flavor = product_definition["variables"]["deployment_flavor"]
        return deployment_flavor

    @staticmethod
    def get_repository() -> str:
        repository = "cervejaria-ambev/" + os.path.basename(os.getcwd())
        return repository

    @staticmethod
    def get_documentation_link() -> str:
        documentation_link = f"https://github.com/cervejaria-ambev/{os.path.basename(os.getcwd())}/docs/project-docs.md"
        return documentation_link

    @staticmethod
    def get_model_description(model_definition: dict) -> dict:
        return model_definition["short_description"]

    @staticmethod
    def get_model_version(model_definition) -> int:
        return model_definition["version"]

    @staticmethod
    def get_mlflow_registry(model_name: str, model_version: int) -> str:
        return f"models:/{model_name}/{model_version}"

    @staticmethod
    def get_model_success_metric(project_metadata: List[Dict]) -> str:
        success_metric = project_metadata[-1]["success_metrics"]
        return success_metric

    @staticmethod
    def get_model_metric_value(project_metadata: List[Dict]) -> float:
        metric_value = project_metadata[-1]["metrics_value"]
        return float(metric_value)

    @staticmethod
    def get_model_created_date(model_artifact, model_name):
        return datetime.strptime(
            model_artifact[model_name]["utc_time_created"], "%Y-%m-%d %H:%M:%S.%f"
        )
