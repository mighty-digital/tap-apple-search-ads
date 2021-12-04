from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream.api import Descriptor, Metadata
from tap_apple_search_ads.stream.concrete import api


class CampaignProvider:
    def campaign(self) -> Schema:
        return {"$id": "campaign", "type": "object"}


def test_campaign_descriptor():
    stream = api.Campaign.from_schema_provider(CampaignProvider())

    expected = Descriptor(
        "campaign",
        "campaign",
        {"$id": "campaign", "type": "object"},
        [Metadata.disabled()],
    )

    assert stream.descriptor() == expected


class CampaignFlatProvider:
    def campaign_flat(self) -> Schema:
        return {"$id": "campaign_flat", "type": "object"}


def test_campaign_flat_descriptor():
    stream = api.CampaignFlat.from_schema_provider(CampaignFlatProvider())

    expected = Descriptor(
        "campaign_flat",
        "campaign_flat",
        {"$id": "campaign_flat", "type": "object"},
        [Metadata.disabled()],
    )

    assert stream.descriptor() == expected
