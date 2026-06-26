from abc import ABC, abstractmethod
from typing import Any

from search.domain.search_profile.entity import SearchProfile


class SearchProfileRepository(ABC):

    @abstractmethod
    async def add(self, entity: SearchProfile) -> None:
        """Create."""

    @abstractmethod
    async def update(self, entity: SearchProfile) -> None:
        """Update."""

    @abstractmethod
    async def get(self, **filters: Any) -> SearchProfile:
        """Get by filters."""

    @abstractmethod
    async def delete(self, entity: SearchProfile) -> None:
        """Delete."""

    @abstractmethod
    async def exists(self, **filters: Any) -> bool:
        """Check if exists."""

    @abstractmethod
    async def get_active_profiles(self) -> list[SearchProfile]:
        """Get all active search profiles."""
