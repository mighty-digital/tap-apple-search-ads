from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass
class Metadata:
    selected: bool = False
    breadcrumb: Tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def disabled(cls):
        return cls()

    def dict(self) -> Dict[str, Any]:
        return {
            "metadata": {"selected": self.selected},
            "breadcrumb": list(self.breadcrumb),
        }
