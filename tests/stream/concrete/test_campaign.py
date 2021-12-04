from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream.api import Descriptor, Metadata
from tap_apple_search_ads.stream.concrete import api


class MockCampaingSchema:
    def campaign(self) -> Schema:
        return {"type": "object"}


def test_init_default():
    stream = api.Campaign.from_schema_provider(MockCampaingSchema())

    expected = Descriptor(
        "campaign", "campaign", {"type": "object"}, [Metadata.disabled()]
    )

    assert stream.descriptor == expected
