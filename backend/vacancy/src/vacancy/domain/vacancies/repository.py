from abc import ABC, abstractmethod
from typing import Any

from vacancy.domain.vacancies.entity import Vacancy
from vacancy.domain.vacancies.value_objects import ProfileId


class VacancyRepository(ABC):

    @abstractmethod
    async def add(self, entity: Vacancy) -> None:
        """Create."""

    @abstractmethod
    async def update(self, entity: Vacancy) -> None:
        """Update."""

    @abstractmethod
    async def get(self, **filters: Any) -> Vacancy:
        """Get by id."""

    @abstractmethod
    async def delete(self, entity: Vacancy) -> None:
        """Delete."""

    @abstractmethod
    async def delete_by_profile_id(self, profile_id: ProfileId) -> None:
        """Delete all vacancies by profile id."""

    @abstractmethod
    async def exists(self, **filters: Any) -> bool:
        """Check if exists."""
