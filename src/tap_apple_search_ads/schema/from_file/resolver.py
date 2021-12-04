from dataclasses import dataclass
from typing import Any, Dict, Optional

from singer.transform import RefResolver
from singer.transform import (
    _resolve_schema_references as singer_resolve_schema_references,
)

from . import Schema, SchemaCollection

DEFS = "$defs"


@dataclass
class Resolver(SchemaCollection):
    collection: SchemaCollection

    def get_schema_by_name(self, name: str) -> Schema:
        schema = self.collection.get_schema_by_name(name)
        return self.resolve(schema)

    def resolve(self, schema: Schema) -> Schema:
        schema = resolve_schema_references(schema, self.parent_schemas)
        schema.pop(DEFS, None)
        return schema

    @property
    def parent_schemas(self) -> Dict[str, Schema]:
        return self.collection.get_schemas()

    def get_schemas(self) -> Dict[str, Schema]:
        resolved: Dict[str, Schema] = {}

        for key, schema in self.parent_schemas.items():
            resolved[key] = self.resolve(schema)

        return resolved


def resolve_schema_references(
    schema: Schema, refs: Optional[Dict[str, Schema]] = None
) -> Dict[str, Any]:
    """resolve_schema_references is a re-implementation of the same function from
    singer.transform. It allows resolution of "allOf" schema element. "allOf" element
    is missing from provided implementation for reasons unknown.
    """

    refs = refs or {}
    return _resolve_schema_references(schema, RefResolver("", schema, store=refs))


def _resolve_schema_references(schema: Schema, resolver: RefResolver) -> Schema:
    if "allOf" in schema:
        for i, element in enumerate(schema["allOf"]):
            schema["allOf"][i] = _resolve_schema_references(element, resolver)

    return singer_resolve_schema_references(schema, resolver)
