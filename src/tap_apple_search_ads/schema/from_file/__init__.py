"""Loading Schema from JSON files."""

from abc import ABC, abstractmethod
from typing import Dict

from tap_apple_search_ads.schema import Schema


class SchemaCollection(ABC):
    @abstractmethod
    def get_schema_by_name(self, name: str) -> Schema:
        ...

    @abstractmethod
    def get_schemas(self) -> Dict[str, Schema]:
        ...
