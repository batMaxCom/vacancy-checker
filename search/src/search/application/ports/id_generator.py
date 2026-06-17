from abc import ABC, abstractmethod
from uuid import UUID


class UUIDGenerator(ABC):
    @abstractmethod
    def next_id(self) -> UUID:
        """Return the next UUID"""


class IntIDGenerator(ABC):
    @abstractmethod
    def next_id(self) -> int:
        """Return the next integer ID"""
