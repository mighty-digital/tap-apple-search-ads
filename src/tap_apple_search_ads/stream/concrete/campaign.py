from dataclasses import dataclass
from typing import Protocol

from tap_apple_search_ads.schema import Schema

from . import ConcreteStreamBase

CAMPAIGN = "campaign"


class SchemaProvider(Protocol):
    def campaign(self) -> Schema:
        ...


@dataclass
class Campaign(ConcreteStreamBase):
    @classmethod
    def from_schema_provider(cls, provider: SchemaProvider):
        return cls(stream=CAMPAIGN, tap_stream_id=CAMPAIGN, schema=provider.campaign())
