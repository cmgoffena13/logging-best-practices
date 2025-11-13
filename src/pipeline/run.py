import logging

from src.sources.base import SourceConfig

logger = logging.getLogger(__name__)


class PipelineRunner:
    def __init__(self, source_config: SourceConfig):
        self.source_config = source_config
        self.source_schema = source_config.source_schema
        self.grain = source_config.grain
        self.audit_query = source_config.audit_query

    def write(self):
        pass

    def audit(self):
        pass

    def publish(self):
        pass

    def run(self):
        self.write()
        self.audit()
        self.publish()
