from dataclasses import dataclass
from typing import Protocol

from tap_apple_search_ads.schema import Schema

from . import ConcreteStreamBase

CAMPAIGN_FLAT = "campaign_flat"


class SchemaProvider(Protocol):
    def campaign_flat(self) -> Schema:
        ...


@dataclass
class CampaignFlat(ConcreteStreamBase):
    @classmethod
    def from_schema_provider(cls, provider: SchemaProvider):
        return cls(
            stream=CAMPAIGN_FLAT,
            tap_stream_id=CAMPAIGN_FLAT,
            schema=provider.campaign_flat(),
        )
