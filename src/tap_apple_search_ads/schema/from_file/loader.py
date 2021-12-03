from dataclasses import InitVar, dataclass, field
from pathlib import Path
from typing import Dict, Union

from . import Schema, SchemaCollection


@dataclass
class Loader(SchemaCollection):
    path: Path = field(init=False)
    schemas: Dict[str, Schema] = field(init=False, default_factory=dict)

    schemas_directory: InitVar[Union[str, Path]]

    def __post_init__(self, schemas_directory: Union[str, Path]) -> None:
        if isinstance(schemas_directory, str):
            schemas_directory = Path(schemas_directory)

        self.path = schemas_directory

    def get_schema_by_name(self, name: str) -> Schema:
        return super().get_schema_by_name(name)
