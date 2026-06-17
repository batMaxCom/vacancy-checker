from typing import Any, cast

from sqlalchemy.ext.asyncio import AsyncSession

from vacancy.domain.vacancies.entity import Vacancy
from vacancy.domain.vacancies.repository import VacancyRepository
from vacancy.infrastructure.persistence.adapters.common.mixins import FilterMixin, QueryMixin
from vacancy.infrastructure.persistence.tables import VACANCY_TABLE


class VacancyRepositoryImpl(VacancyRepository, QueryMixin, FilterMixin):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, entity: Vacancy) -> None:
        self.__session.add(entity)

    async def update(self, entity: Vacancy) -> None:
        await self.__session.merge(entity)

    async def get(self, **filters: Any) -> Vacancy:
        query = self._get_query(VACANCY_TABLE)
        query = self._add_filters(VACANCY_TABLE, query, **filters)
        result = await self.__session.execute(query)
        return cast("Vacancy", result.scalar_one())

    async def delete(self, entity: Vacancy) -> None:
        await self.__session.delete(entity)

    async def exists(self, **filters: Any) -> bool:
        query = self._get_query(VACANCY_TABLE, ["id"])
        query = self._add_filters(VACANCY_TABLE, query, **filters)
        result = await self.__session.execute(query)
        return result.scalar() is not None
