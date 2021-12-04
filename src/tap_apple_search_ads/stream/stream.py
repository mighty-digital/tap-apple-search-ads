from abc import ABC, abstractmethod

from .descriptor import Descriptor


class Stream(ABC):
    @abstractmethod
    def descriptor(self) -> Descriptor:
        ...
