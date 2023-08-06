from typing import List, Type, Union

from pyiris.ingestion.pipeline.pipeline import Pipeline


class PipelineService(object):
    def __init__(self, pipelines: List[Type[Union[Pipeline]]]):
        self.pipelines = pipelines

    def run_all(self):
        for pipeline in self.pipelines:
            pipeline.run()
