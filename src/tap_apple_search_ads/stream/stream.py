from abc import ABC, abstractmethod

from .descriptor import Descriptor


class Stream(ABC):
    @abstractmethod
    def descriptor(self) -> Descriptor:
        ...

    @abstractmethod
    def set_descriptor(self, descriptor: Descriptor):
        ...
