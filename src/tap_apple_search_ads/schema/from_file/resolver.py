from dataclasses import dataclass

from . import Schema, SchemaCollection

DEFS = "$defs"


@dataclass
class Resolver(SchemaCollection):
    collection: SchemaCollection

    def get_schema_by_name(self, name: str) -> Schema:
        schema = self.collection.get_schema_by_name(name)

        schema.pop(DEFS, None)

        return schema
