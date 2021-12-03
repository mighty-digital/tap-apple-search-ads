"""Loading Schema from JSON files."""

from abc import ABC, abstractmethod
from typing import Any, Dict

Schema = Dict[str, Any]


class SchemaCollection(ABC):
    @abstractmethod
    def get_schema_by_name(self, name: str) -> Schema:
        ...

    @abstractmethod
    def get_schemas(self) -> Dict[str, Schema]:
        ...
