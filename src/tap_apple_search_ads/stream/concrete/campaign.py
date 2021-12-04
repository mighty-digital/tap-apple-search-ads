from dataclasses import dataclass
from typing import Protocol

from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream.api import Descriptor, Metadata, Stream

CAMPAIGN = "campaign"


class SchemaProvider(Protocol):
    def campaign(self) -> Schema:
        ...


@dataclass
class Campaign(Stream):
    schema: Schema

    @classmethod
    def from_schema_provider(cls, provider: SchemaProvider):
        return cls(schema=provider.campaign())

    @property
    def descriptor(self) -> Descriptor:
        return Descriptor(
            stream=CAMPAIGN,
            tap_stream_id=CAMPAIGN,
            schema=self.schema,
            metadata=[Metadata.disabled()],
        )
