from pydantic import BaseModel, Field

from src.sources.base import SourceConfig


class SourceRegistry(BaseModel):
    sources: list[SourceConfig] = Field(default_factory=list)

    def add_sources(self, sources: list[SourceConfig]) -> None:
        self.sources.extend(sources)

    def get_source_configs(self) -> list[SourceConfig]:
        return self.sources
