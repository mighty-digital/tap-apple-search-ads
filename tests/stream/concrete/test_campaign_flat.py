from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream.api import Descriptor, Metadata
from tap_apple_search_ads.stream.concrete import api


class MockProvider:
    def campaign_flat(self) -> Schema:
        return {"type": "object"}


def test_init_default():
    stream = api.CampaignFlat.from_schema_provider(MockProvider())

    expected = Descriptor(
        "campaign_flat", "campaign_flat", {"type": "object"}, [Metadata.disabled()]
    )

    assert stream.descriptor() == expected
