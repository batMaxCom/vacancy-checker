from abc import ABC, abstractmethod
from typing import Any

from search.domain.search_job.entity import SearchJob
from search.domain.search_profile.value_objects import SearchProfileId


class SearchJobRepository(ABC):

    @abstractmethod
    async def add(self, entity: SearchJob) -> None:
        """Create."""

    @abstractmethod
    async def update(self, entity: SearchJob) -> None:
        """Update."""

    @abstractmethod
    async def get(self, **filters: Any) -> SearchJob:
        """Get by filters."""

    @abstractmethod
    async def delete(self, entity: SearchJob) -> None:
        """Delete."""

    @abstractmethod
    async def exists(self, **filters: Any) -> bool:
        """Check if exists."""

    @abstractmethod
    async def get_all_by_profile_id(self, profile_id: SearchProfileId) -> list[SearchJob]:
        """Get all by profile_id."""
