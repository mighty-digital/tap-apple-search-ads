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

    def get_schemas(self) -> Dict[str, Schema]:
        return self.schemas


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


@pytest.fixture
def defs_used_collection() -> MockSchemaCollection:
    return MockSchemaCollection(
        {
            "a.json": {
                "type": "object",
                "properties": {"o": {"$ref": "o.json"}, "d": {"$ref": "#/$defs/d"}},
                "$defs": {"d": {"type": "object"}},
            },
            "o.json": {"type": "object"},
        }
    )


def test_resolver_resolves(defs_used_collection: MockSchemaCollection):
    resolver = api.Resolver(defs_used_collection)

    expected = {
        "type": "object",
        "properties": {"o": {"type": "object"}, "d": {"type": "object"}},
    }

    schema = resolver.get_schema_by_name("a.json")

    assert schema == expected


@pytest.fixture
def defs_used_allof_collection() -> MockSchemaCollection:
    return MockSchemaCollection(
        {
            "a.json": {
                "type": "object",
                "properties": {"o": {"$ref": "o.json"}},
            },
            "o.json": {"type": "object"},
            "b.json": {
                "allOf": [
                    {"type": "object", "properties": {"c": {"type": "object"}}},
                    {"$ref": "a.json"},
                    {"$ref": "o.json"},
                ]
            },
        }
    )


def test_resolver_resolves_allof(defs_used_allof_collection: MockSchemaCollection):
    resolver = api.Resolver(defs_used_allof_collection)

    expected = {
        "allOf": [
            {"type": "object", "properties": {"c": {"type": "object"}}},
            {"type": "object", "properties": {"o": {"type": "object"}}},
            {"type": "object"},
        ]
    }

    schema = resolver.get_schema_by_name("b.json")

    assert schema == expected


def test_resolver_resolves_all_schemas(
    defs_used_allof_collection: MockSchemaCollection,
):
    resolver = api.Resolver(defs_used_allof_collection)

    expected = {
        "a.json": {"type": "object", "properties": {"o": {"type": "object"}}},
        "o.json": {"type": "object"},
        "b.json": {
            "allOf": [
                {"type": "object", "properties": {"c": {"type": "object"}}},
                {"type": "object", "properties": {"o": {"type": "object"}}},
                {"type": "object"},
            ]
        },
    }

    schemas = resolver.get_schemas()

    assert schemas == expected
