import logging
from typing import Any, Dict, Iterator

from opentelemetry import trace

from src.pipeline.read.factory import ReaderFactory
from src.pipeline.validate.validator import Validator
from src.sources.base import SourceConfig

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


class PipelineRunner:
    def __init__(self, source_config: SourceConfig):
        self.source_config = source_config
        self.source_schema = source_config.source_schema
        self.grain = source_config.grain
        self.audit_query = source_config.audit_query
        self.validator = Validator(self.source_config)

    def read_data(self) -> Iterator[list[Dict[str, Any]]]:
        logger.info(f"Reading data from {self.source_config.name}")
        reader = ReaderFactory.get_reader(self.source_config)
        for batch in reader.read():
            yield batch

    def validate_data(self, data: Iterator[list[Dict[str, Any]]]):
        logger.info(f"Validating data for {self.source_config.name}")
        for batch in data:
            yield self.validator.validate(batch)

    def write_data(self):
        logger.info(f"Writing data to stage_{self.source_config.name}")

    def audit_data(self):
        logger.info(f"Auditing data for stage_{self.source_config.name}")

    def publish_data(self):
        logger.info(f"Publishing data for {self.source_config.name}")

    def run(self):
        with tracer.start_as_current_span(
            f"Pipeline: {self.source_config.name}",
        ):
            result = None
            try:
                # Chain Iterators to Stream Batch Data
                self.write_data(self.validate_data(self.read_data()))
                self.audit_data()
                self.publish_data()
            except Exception as e:
                logger.exception(
                    f"Error running pipeline for {self.source_config.name}: {e}"
                )
                result = (False, self.source_config.name)
                return result
            result = (True, self.source_config.name)
            return result
