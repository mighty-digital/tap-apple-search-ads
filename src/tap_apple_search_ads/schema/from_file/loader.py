import json
from dataclasses import InitVar, dataclass, field
from pathlib import Path
from typing import Dict, Union

from . import Schema, SchemaCollection

JSON = [".json"]


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
        if not self.schemas:
            self.schemas = load_json_files(self.path)

        return self.schemas[name]


def load_json_files(directory: Path) -> Dict[str, Schema]:
    if not directory.exists():
        raise LoaderError("path {} does not exist".format(directory))

    if not directory.is_dir():
        raise LoaderError("path {} is not a directory".format(directory))

    json_files: Dict[str, Schema] = {}
    for file in directory.iterdir():
        if not file.is_file():
            continue

        if file.suffix not in JSON:
            continue

        with open(file) as stream:
            json_files[file.stem] = json.load(stream)

    if not json_files:
        raise LoaderError("directory {} does not contain any JSON files")

    return json_files


class LoaderError(Exception):
    """Schema loading failed"""
