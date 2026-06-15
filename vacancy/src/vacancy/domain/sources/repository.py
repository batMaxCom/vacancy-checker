from abc import ABC, abstractmethod
from typing import Any

from vacancy.domain.sources.entity import Source


class SourceRepository(ABC):

    @abstractmethod
    async def add(self, entity: Source) -> None:
        """Create."""

    @abstractmethod
    async def update(self, entity: Source) -> None:
        """Update."""

    @abstractmethod
    async def get(self, **filters: Any) -> Source:
        """Get by id."""

    @abstractmethod
    async def delete(self, entity: Source) -> None:
        """Delete."""

    @abstractmethod
    async def exists(self, **filters: Any) -> bool:
        """Check if exists."""
