from dataclasses import dataclass, field
from typing import List, Optional

from tap_apple_search_ads.schema import Schema

from .metadata import Metadata


@dataclass
class Descriptor:
    stream: str
    tap_stream_id: str
    schema: Schema
    metadata: List[Metadata] = field(default_factory=list)

    @classmethod
    def disabled(cls, stream: str, schema: Schema, tap_stream_id: Optional[str] = None):
        if tap_stream_id is None:
            tap_stream_id = stream

        return cls(stream, tap_stream_id, schema, [Metadata.disabled()])
