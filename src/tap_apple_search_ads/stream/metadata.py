from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class Metadata:
    enabled: bool = False
    breadcrumb: Tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def disabled(cls):
        return cls()
