from abc import ABC, abstractmethod
from typing import Iterable

from . import Record
from .descriptor import Descriptor


class Stream(ABC):
    @abstractmethod
    def descriptor(self) -> Descriptor:
        ...

    @abstractmethod
    def set_descriptor(self, descriptor: Descriptor):
        ...

    @abstractmethod
    def sync(self) -> Iterable[Record]:
        ...
