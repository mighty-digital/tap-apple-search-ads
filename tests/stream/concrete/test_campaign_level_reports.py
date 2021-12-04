from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream import concrete as streams
from tap_apple_search_ads.stream.api import Descriptor, Metadata


class ClrProvider:
    def campaign_level_reports(self) -> Schema:
        return {"$id": "campaign_level_reports", "type": "object"}


def test_campaign_level_reports_descriptor():
    stream = streams.CampaignLevelReports.from_schema_provider(ClrProvider())

    expected = Descriptor(
        "campaign_level_reports",
        "campaign_level_reports",
        {"$id": "campaign_level_reports", "type": "object"},
        [Metadata.disabled()],
    )

    assert stream.descriptor() == expected


class EsrProvider:
    def campaign_level_reports_extended_spend_row(self) -> Schema:
        return {"$id": "campaign_level_reports_esr", "type": "object"}


def test_campaign_level_reports_esr_descriptor():
    stream = streams.ExtendedSpendRow.from_schema_provider(EsrProvider())

    expected = Descriptor(
        "campaign_level_reports_extended_spend_row",
        "campaign_level_reports_extended_spend_row",
        {"$id": "campaign_level_reports_esr", "type": "object"},
        [Metadata.disabled()],
    )

    assert stream.descriptor() == expected


class EsrFlatProvider:
    def campaign_level_reports_extended_spend_row_flat(self) -> Schema:
        return {"$id": "campaign_level_reports_esr_flat", "type": "object"}


def test_campaign_level_reports_esr_flat_descriptor():
    stream = streams.ExtendedSpendRowFlat.from_schema_provider(EsrFlatProvider())

    expected = Descriptor(
        "campaign_level_reports_extended_spend_row_flat",
        "campaign_level_reports_extended_spend_row_flat",
        {"$id": "campaign_level_reports_esr_flat", "type": "object"},
        [Metadata.disabled()],
    )

    assert stream.descriptor() == expected
