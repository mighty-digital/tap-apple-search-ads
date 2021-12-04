from dataclasses import dataclass
from typing import Protocol

from tap_apple_search_ads.schema import Schema

from . import ConcreteStreamBase

CAMPAIGN = "campaign"
CAMPAIGN_FLAT = "campaign_flat"


class CampaignSchemaProvider(Protocol):
    def campaign(self) -> Schema:
        ...


@dataclass
class Campaign(ConcreteStreamBase):
    @classmethod
    def from_schema_provider(cls, provider: CampaignSchemaProvider):
        return cls(stream=CAMPAIGN, tap_stream_id=CAMPAIGN, schema=provider.campaign())


class CampaignFlatSchemaProvider(Protocol):
    def campaign_flat(self) -> Schema:
        ...


@dataclass
class CampaignFlat(ConcreteStreamBase):
    @classmethod
    def from_schema_provider(cls, provider: CampaignFlatSchemaProvider):
        return cls(
            stream=CAMPAIGN_FLAT,
            tap_stream_id=CAMPAIGN_FLAT,
            schema=provider.campaign_flat(),
        )
