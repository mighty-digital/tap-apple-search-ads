from dataclasses import dataclass
from typing import Dict
from unittest import mock

from tap_apple_search_ads.schema import Schema, from_file
from tap_apple_search_ads.schema.from_file import api


@dataclass
class MockSchemaCollection(from_file.SchemaCollection):
    schemas: Dict[str, Schema]

    def get_schema_by_name(self, name: str) -> Schema:
        return self.schemas[name]

    def get_schemas(self) -> Dict[str, Schema]:
        return self.schemas


def test_facade_init():
    collection = MockSchemaCollection({})
    facade = api.Facade(collection)
    assert facade.collection is collection


def test_campaign():
    collection = MockSchemaCollection({"Campaign.json": mock.sentinel.schema})
    facade = api.Facade(collection)
    schema = facade.campaign()
    assert schema is mock.sentinel.schema


def test_campaign_flat():
    collection = MockSchemaCollection({"Campaign_Flat.json": mock.sentinel.schema})
    facade = api.Facade(collection)
    schema = facade.campaign_flat()
    assert schema is mock.sentinel.schema


def test_campaign_level_reports():
    collection = MockSchemaCollection({"Row.json": mock.sentinel.schema})
    facade = api.Facade(collection)
    schema = facade.campaign_level_reports()
    assert schema is mock.sentinel.schema


def test_campaign_level_reports_extended_spend_row():
    collection = MockSchemaCollection(
        {"ExtendedSpendRow_campaignId.json": mock.sentinel.schema}
    )
    facade = api.Facade(collection)
    schema = facade.campaign_level_reports_extended_spend_row()
    assert schema is mock.sentinel.schema


def test_campaign_level_reports_extended_spend_row_flat():
    collection = MockSchemaCollection(
        {"ExtendedSpendRow_campaignId_Flat.json": mock.sentinel.schema}
    )
    facade = api.Facade(collection)
    schema = facade.campaign_level_reports_extended_spend_row_flat()
    assert schema is mock.sentinel.schema
