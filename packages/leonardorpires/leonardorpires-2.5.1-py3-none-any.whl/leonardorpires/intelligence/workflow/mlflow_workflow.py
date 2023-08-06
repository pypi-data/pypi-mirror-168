from typing import Any, List

import mlflow

from pyiris.intelligence.workflow.workflow import Workflow


class MlflowWorkflow(Workflow):
    """
    ! Class not yet implemented !
    This class aims to wrap up a pipeline that will be tied to the "main" entrypoint on the mlflow MLProject file.
    With it, the user will be able to chain together the modules execution sequence in a declarative and replicable
    way.
    """

    def __init__(self, modules: List[Any] = None):
        self.modules = modules

    def run(self):
        with mlflow.start_run():
            for module in self.modules:
                module.run()
            mlflow.end_run()
