import logging
from typing import Any, Dict, Iterator

from pydantic import TypeAdapter, ValidationError

from src.sources.base import SourceConfig

logger = logging.getLogger(__name__)


class Validator:
    def __init__(self, source_config: SourceConfig):
        self.source_config = source_config
        self.adapter = TypeAdapter(self.source_config.source_schema)
        self.total_records = 0
        self.invalid_records = 0

    def validate(
        self, data: Iterator[list[Dict[str, Any]]]
    ) -> Iterator[list[Dict[str, Any]]]:
        for batch in data:
            for record in batch:
                self.total_records += 1
                try:
                    record = self.adapter.validate_python(record).model_dump()
                except ValidationError as e:
                    self.invalid_records += 1
                    logger.error(f"Validation error for record: {record}: {e}")
                    continue
            yield batch
