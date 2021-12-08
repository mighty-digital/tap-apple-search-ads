from unittest.mock import sentinel

from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream import concrete as stream
from tap_apple_search_ads.stream.core import Descriptor, Metadata


class SchemaProvider:
    def campaign(self) -> Schema:
        return {"$id": "campaign", "type": "object", "properties": sentinel.c}

    def campaign_flat(self) -> Schema:
        return {"$id": "campaign_flat", "type": "object", "properties": sentinel.cf}

    def campaign_level_reports(self) -> Schema:
        return {
            "$id": "campaign_level_reports",
            "type": "object",
            "properties": sentinel.clr,
        }

    def campaign_level_reports_extended_spend_row(self) -> Schema:
        return {
            "$id": "campaign_level_reports_esr",
            "type": "object",
            "properties": sentinel.clresr,
        }

    def campaign_level_reports_extended_spend_row_flat(self) -> Schema:
        return {
            "$id": "campaign_level_reports_esr_flat",
            "type": "object",
            "properties": sentinel.clresrf,
        }


def test_campaign():
    factory = stream.DescriptorFactory(SchemaProvider())

    assert factory.campaign() == Descriptor(
        "campaign",
        "campaign",
        {
            "$id": "campaign",
            "type": "object",
            "properties": sentinel.c,
        },
        [Metadata.disabled()],
    )


def test_campaign_flat_descriptor():
    factory = stream.DescriptorFactory(SchemaProvider())

    assert factory.campaign_flat() == Descriptor(
        "campaign_flat",
        "campaign_flat",
        {"$id": "campaign_flat", "type": "object", "properties": sentinel.cf},
        [Metadata.disabled()],
    )


def test_campaign_level_reports():
    factory = stream.DescriptorFactory(SchemaProvider())

    assert factory.campaign_level_reports() == Descriptor(
        "campaign_level_reports",
        "campaign_level_reports",
        {"$id": "campaign_level_reports", "type": "object", "properties": sentinel.clr},
        [Metadata.disabled()],
    )


def test_campaign_level_reports_extended_spend_row():
    factory = stream.DescriptorFactory(SchemaProvider())

    assert factory.campaign_level_reports_extended_spend_row() == Descriptor(
        "campaign_level_reports_extended_spend_row",
        "campaign_level_reports_extended_spend_row",
        {
            "$id": "campaign_level_reports_esr",
            "type": "object",
            "properties": sentinel.clresr,
        },
        [Metadata.disabled()],
    )


def test_campaign_level_reports_extended_spend_row_flat():
    factory = stream.DescriptorFactory(SchemaProvider())

    assert factory.campaign_level_reports_extended_spend_row_flat() == Descriptor(
        "campaign_level_reports_extended_spend_row_flat",
        "campaign_level_reports_extended_spend_row_flat",
        {
            "$id": "campaign_level_reports_esr_flat",
            "type": "object",
            "properties": sentinel.clresrf,
        },
        [Metadata.disabled()],
    )
