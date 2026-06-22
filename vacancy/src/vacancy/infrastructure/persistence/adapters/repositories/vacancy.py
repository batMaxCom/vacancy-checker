from typing import Any, cast

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from vacancy.domain.vacancies.entity import Vacancy
from vacancy.domain.vacancies.repository import VacancyRepository
from vacancy.domain.vacancies.value_objects import ProfileId
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
        query = self._get_query(Vacancy)
        query = self._add_filters(VACANCY_TABLE, query, **filters)
        result = await self.__session.execute(query)
        return cast("Vacancy", result.scalar_one())

    async def delete(self, entity: Vacancy) -> None:
        await self.__session.delete(entity)

    async def delete_by_profile_id(self, profile_id: ProfileId) -> None:
        await self.__session.execute(
            delete(VACANCY_TABLE).where(VACANCY_TABLE.c.profile_id == profile_id)
        )

    async def exists(self, **filters: Any) -> bool:
        query = self._get_query(VACANCY_TABLE, ["id"])
        query = self._add_filters(VACANCY_TABLE, query, **filters)
        result = await self.__session.execute(query)
        return result.scalar() is not None
