from typing import Dict, Optional

import yaml
from mlflow.tracking import MlflowClient


class MlFlow(object):
    def __init__(self, client: Optional[MlflowClient] = None):
        self.client = client or MlflowClient()

    def get_model_artifact(self, model_name: str, model_version: int) -> Dict:
        local_dir = "/tmp"
        artifact_path = "model"
        mlflow_objects_list = self.client.search_model_versions(f"name='{model_name}'")
        current_version_object = list(
            filter(
                lambda object: object.version == str(model_version),
                mlflow_objects_list,
            )
        )

        current_version_run_id = current_version_object[0].run_id
        local_path = self.client.download_artifacts(
            current_version_run_id, f"{artifact_path}/MLmodel", local_dir
        )

        with open(local_path, "r") as f:
            model_artifact = {model_name: yaml.load(f, Loader=yaml.FullLoader)}

        return model_artifact
