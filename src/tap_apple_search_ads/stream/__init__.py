"""Implementation of Singer's Stream abstraction (and related items)."""

from typing import Any, Dict

Record = Dict[str, Any]


class StreamError(Exception):
    pass
