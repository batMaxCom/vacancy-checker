from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from search.application.common.dto import FoundVacancyDto
    from search.domain.search_profile.value_objects import Keyword


class VacancySearchProvider(ABC):
    """Интерфейс поиска вакансий."""

    @abstractmethod
    async def search(
        self,
        keywords: list[Keyword],
    ) -> list[FoundVacancyDto]:
        """Выполнить поиск вакансий по ключевым словам."""
