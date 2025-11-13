from typing import Optional, Type

from pydantic import BaseModel, ConfigDict


class TableModel(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)


class SourceConfig(BaseModel):
    name: str
    grain: list[str]
    source_schema: Type[TableModel]
    audit_query: Optional[str] = None
