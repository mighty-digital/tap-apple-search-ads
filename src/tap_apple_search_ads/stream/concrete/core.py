"""Concrete Stream instances - provide actual data sync."""

from dataclasses import dataclass

from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream.api import Descriptor, Metadata, Stream


@dataclass
class ConcreteStreamBase(Stream):
    stream: str
    tap_stream_id: str
    schema: Schema

    def descriptor(self) -> Descriptor:
        return Descriptor(
            stream=self.stream,
            tap_stream_id=self.tap_stream_id,
            schema=self.schema,
            metadata=[Metadata.disabled()],
        )
