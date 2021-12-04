from dataclasses import dataclass
from typing import Protocol

from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream.api import Descriptor, Metadata, Stream

CAMPAIGN_FLAT = "campaign_flat"


class SchemaProvider(Protocol):
    def campaign_flat(self) -> Schema:
        ...


@dataclass
class CampaignFlat(Stream):
    schema: Schema

    @classmethod
    def from_schema_provider(cls, provider: SchemaProvider):
        return cls(schema=provider.campaign_flat())

    @property
    def descriptor(self) -> Descriptor:
        return Descriptor(
            stream=CAMPAIGN_FLAT,
            tap_stream_id=CAMPAIGN_FLAT,
            schema=self.schema,
            metadata=[Metadata.disabled()],
        )
