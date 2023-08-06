from abc import ABC, abstractmethod

from pyiris.ingestion.pipeline.pipeline_monitor import PipelineMonitor


@PipelineMonitor()
class Pipeline(ABC):
    @staticmethod
    @abstractmethod
    def run():
        pass
