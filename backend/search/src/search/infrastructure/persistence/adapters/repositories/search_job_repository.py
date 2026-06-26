from typing import cast

from sqlalchemy import exists as sa_exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from search.domain.search_job.entity import SearchJob
from search.domain.search_job.repository import SearchJobRepository
from search.domain.search_profile.value_objects import SearchProfileId
from search.infrastructure.persistence.adapters.common.mixins import FilterMixin, QueryMixin
from search.infrastructure.persistence.tables import SEARCH_JOB_TABLE


class SearchJobRepositoryImpl(QueryMixin, FilterMixin, SearchJobRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, entity: SearchJob) -> None:
        self.__session.add(entity)

    async def update(self, entity: SearchJob) -> None:
        await self.__session.merge(entity)

    async def get(self, **filters: object) -> SearchJob:
        query = self._get_query(SearchJob)
        query = self._add_filters(SEARCH_JOB_TABLE, query, **filters)
        result = await self.__session.execute(query)
        return cast(SearchJob, result.scalars().one())

    async def delete(self, entity: SearchJob) -> None:
        await self.__session.delete(entity)

    async def exists(self, **filters: object) -> bool:
        inner_query = select(SEARCH_JOB_TABLE)
        inner_query = self._add_filters(SEARCH_JOB_TABLE, inner_query, **filters)
        stmt = select(sa_exists(inner_query))
        result = await self.__session.execute(stmt)
        return bool(result.scalar())

    async def get_all_by_profile_id(self, profile_id: SearchProfileId) -> list[SearchJob]:
        query = self._get_query(SearchJob)
        query = self._add_filters(SEARCH_JOB_TABLE, query, profile_id=profile_id)
        result = await self.__session.execute(query)
        return list(result.scalars().all())
