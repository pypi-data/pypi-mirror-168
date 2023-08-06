from pyiris.infrastructure.integration.database.repository_integration import (
    RepositoryIntegration,
)
from pyiris.infrastructure.service.metadata.entity.model_entity import Model
from pyiris.infrastructure.service.metadata.entity.model_version_entity import (
    ModelVersion,
)
from pyiris.infrastructure.service.monitor.log.logger import Logger

logger = Logger(__name__)


class ModelRepository(RepositoryIntegration):
    """
    A class responsible for executing operations in database direct to
    pyiris.infrastructure.service.metadata.entity.model.Model table
    and pyiris.infrastructure.service.metadata.entity.model_version.ModelVersion table.
    """

    def __init__(self, session=None):
        super().__init__(session)

    def add_if_not_exist(self, model: Model):
        current_model = (
            self.session.query(Model)
            .filter_by(
                name=model.name,
                deployment_flavor=model.deployment_flavor,
                repository=model.repository,
                description=model.description,
                project_docs_url=model.project_docs_url,
            )
            .first()
        )

        if not current_model:
            self.add_all(tables=[model])
            logger.info(
                f"Registry from {model.name} added to the 'iris intelligence' tables."
            )
            self.session.commit()
            return model
        else:
            logger.info(
                f"This registry from {model.name} already exists in the 'model' table."
            )
            model.id = current_model.id
            for model_version in model.versions:
                current_model_version = (
                    self.session.query(ModelVersion)
                    .filter_by(
                        version=model_version.version,
                        mlflow_registry=model_version.mlflow_registry,
                        commit_hash=model_version.commit_hash,
                        success_metric=model_version.success_metric,
                        metric_value=model_version.metric_value,
                        model_input=model_version.model_input,
                        model_output=model_version.model_output,
                        mlflow_created_date=model_version.mlflow_created_date,
                    )
                    .first()
                )

                if not current_model_version:
                    logger.info(
                        f"Registry from model_version about {model.name} has been updated"
                    )
                    model_version.model_id = model.id
                    self.session.merge(model_version)
                    self.session.commit()
                    return model
                else:
                    logger.info(
                        f" Registry from model_version: {model_version.version} already exists."
                    )
