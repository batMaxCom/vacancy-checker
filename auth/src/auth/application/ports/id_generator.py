from abc import ABC, abstractmethod
from uuid import UUID


class UUIDGenerator(ABC):
    @abstractmethod
    def next_id(self) -> UUID:
        """Return the next UUID"""
