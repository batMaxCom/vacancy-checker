from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from search.application.common.dto import FoundVacancyDto
    from search.domain.search_profile.entity import SearchProfile


class VacancySearcher(ABC):
    """Сервис поиска вакансий."""

    @abstractmethod
    async def search_by_profile(
        self,
        profile: SearchProfile,
    ) -> list[FoundVacancyDto]:
        """..."""
