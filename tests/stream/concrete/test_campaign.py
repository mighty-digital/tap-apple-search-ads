import json
from pathlib import Path
from typing import Any

from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream import concrete as streams
from tap_apple_search_ads.stream.concrete.campaign import GetAllCampaignsResponse
from tap_apple_search_ads.stream.core import Descriptor, Metadata

TESTDATA = Path(__file__).absolute().parent / "testdata"


class CampaignProvider:
    def campaign(self) -> Schema:
        return {"$id": "campaign", "type": "object"}


def test_campaign_descriptor():
    stream = streams.Campaign.from_schema_provider(CampaignProvider())
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
    stream = streams.CampaignFlat.from_schema_provider(CampaignFlatProvider())
    expected = Descriptor(
        "campaign_flat",
        "campaign_flat",
        {"$id": "campaign_flat", "type": "object"},
        [Metadata.disabled()],
    )
    assert stream.descriptor() == expected


class CampaignApi:
    def get_all_campaigns(self) -> GetAllCampaignsResponse:
        return get_test_file("get-all-campaigns-response.json")

    def expected_campaigns(self):
        return get_test_file("expected-campaigns.json")

    def expected_campaigns_flat(self):
        return get_test_file("expected-campaigns-flat.json")


def get_test_file(filename: str) -> Any:
    data_path = TESTDATA / filename
    with open(data_path) as stream:
        data = json.load(stream)
    return data


def test_campaign_sync():
    api = CampaignApi()
    stream = streams.Campaign.from_schema_provider(CampaignProvider())
    stream.set_api(api)
    expected = api.expected_campaigns()
    assert stream.sync() == expected


def test_campaign_flat_sync():
    api = CampaignApi()
    campaign = streams.Campaign.from_schema_provider(CampaignProvider())
    campaign.set_api(api)
    stream = streams.CampaignFlat.from_schema_provider(CampaignFlatProvider())
    stream.set_campaign(campaign)
    expected = api.expected_campaigns_flat()
    assert stream.sync() == expected
