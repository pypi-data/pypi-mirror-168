from typing import List

from pyiris.intelligence.workflow.workflow import Workflow


class PredictWorkflow(Workflow):
    """
    ! Class not yet implemented !
    This class intends to make it easier to chain together multiple steps for a predict job execution. It is going to be
    replaced with the current 'main.py' file that currently is using Databricks' magic %run commands to define a
    prediction job
    """

    def __init__(self, steps: List[str] = None):
        self.steps = steps

    def run(self):
        for step in self.steps:
            step.run()
