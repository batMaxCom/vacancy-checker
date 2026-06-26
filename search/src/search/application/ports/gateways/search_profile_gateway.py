from abc import ABC, abstractmethod

from search.application.common.dto.search_profile_dto import SearchProfileDto
from search.domain.search_profile.value_objects import SearchProfileId
from search.domain.shared_kernel.value_objects import UserId


class SearchProfileGateway(ABC):

    @abstractmethod
    async def get_by_id(self, search_profile_id: SearchProfileId) -> SearchProfileDto | None:
        """Get search profile by id."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UserId) -> list[SearchProfileDto]:
        """Get all search profiles for a user."""

    @abstractmethod
    async def get_active_profiles(self) -> list[SearchProfileDto]:
        """Get all active search profiles."""
