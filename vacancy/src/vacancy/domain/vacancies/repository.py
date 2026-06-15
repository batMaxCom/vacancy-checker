from abc import ABC, abstractmethod
from typing import Any

from vacancy.domain.vacancies.entity import Vacancy


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
    async def exists(self, **filters: Any) -> bool:
        """Check if exists."""
