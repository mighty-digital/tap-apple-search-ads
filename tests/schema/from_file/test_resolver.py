from dataclasses import dataclass
from typing import Dict

import pytest

from tap_apple_search_ads.schema import from_file
from tap_apple_search_ads.schema.from_file import api
from tap_apple_search_ads.schema.from_file.api import Schema


@dataclass
class MockSchemaCollection(from_file.SchemaCollection):
    schemas: Dict[str, Schema]

    def get_schema_by_name(self, name: str) -> Schema:
        return self.schemas[name]


@pytest.fixture
def basic_collection() -> MockSchemaCollection:
    return MockSchemaCollection(
        {
            "a": {"type": "object"},
            "b": {"type": "object"},
            "c": {"type": "object"},
        }
    )


def test_resolver_init(basic_collection: MockSchemaCollection):
    resolver = api.Resolver(basic_collection)

    assert resolver.collection is basic_collection


def test_resolver_basic(basic_collection: MockSchemaCollection):
    resolver = api.Resolver(basic_collection)

    expected = {"type": "object"}
    for name in list("abc"):
        schema = resolver.get_schema_by_name(name)
        assert schema == expected


@pytest.fixture
def defs_collection() -> MockSchemaCollection:
    return MockSchemaCollection(
        {
            "a": {"type": "object", "$defs": {"o": {"type": "object"}}},
            "b": {"type": "object", "$defs": {"o": {"type": "object"}}},
            "c": {"type": "object", "$defs": {"o": {"type": "object"}}},
        }
    )


def test_resolver_removes_defs(defs_collection: MockSchemaCollection):
    resolver = api.Resolver(defs_collection)

    expected = {"type": "object"}
    for name in list("abc"):
        schema = resolver.get_schema_by_name(name)
        assert schema == expected
