"""Concrete Stream instances - provide actual data sync."""

from dataclasses import dataclass, field
from typing import Iterable, Optional

from tap_apple_search_ads.schema import Schema
from tap_apple_search_ads.stream.core import Descriptor, Metadata, Record, Stream


@dataclass
class ConcreteStreamBase(Stream):
    stream: str
    tap_stream_id: str
    schema: Schema

    _descriptor: Optional[Descriptor] = field(init=False, default=None)

    def descriptor(self) -> Descriptor:
        if self._descriptor is not None:
            return self._descriptor

        return default_descriptor(self)

    def set_descriptor(self, descriptor: Optional[Descriptor]):
        """set_descriptor allows to set an updated Descriptor instance as a Stream's
        Descriptor.
        Reverting to default Descriptor is as easy as Stream#set_descriptor(None).
        """

        self._descriptor = descriptor

    def sync(self) -> Iterable[Record]:
        return super().sync()


def default_descriptor(stream: ConcreteStreamBase) -> Descriptor:
    return Descriptor(
        stream=stream.stream,
        tap_stream_id=stream.tap_stream_id,
        schema=stream.schema,
        metadata=[Metadata.disabled()],
    )
