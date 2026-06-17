from abc import ABC, abstractmethod

from search.application.common.dto.search_job_dto import SearchJobDto
from search.domain.search_job.value_objects import SearchJobId
from search.domain.search_profile.value_objects import SearchProfileId


class SearchJobGateway(ABC):

    @abstractmethod
    async def get_by_id(self, search_job_id: SearchJobId) -> SearchJobDto | None:
        """Get search job by id."""

    @abstractmethod
    async def get_by_profile_id(self, profile_id: SearchProfileId) -> list[SearchJobDto]:
        """Get all search jobs for a profile."""
