from typing import cast

from sqlalchemy import exists as sa_exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from search.domain.search_profile.entity import SearchProfile
from search.domain.search_profile.repository import SearchProfileRepository
from search.infrastructure.persistence.adapters.common.mixins import FilterMixin, QueryMixin
from search.infrastructure.persistence.tables import SEARCH_PROFILE_TABLE


class SearchProfileRepositoryImpl(QueryMixin, FilterMixin, SearchProfileRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, entity: SearchProfile) -> None:
        self.__session.add(entity)

    async def update(self, entity: SearchProfile) -> None:
        await self.__session.merge(entity)

    async def get(self, **filters: object) -> SearchProfile:
        query = self._get_query(SearchProfile)
        query = self._add_filters(SEARCH_PROFILE_TABLE, query, **filters)
        result = await self.__session.execute(query)
        return cast(SearchProfile, result.scalars().one())

    async def delete(self, entity: SearchProfile) -> None:
        await self.__session.delete(entity)

    async def exists(self, **filters: object) -> bool:
        inner_query = select(SEARCH_PROFILE_TABLE)
        inner_query = self._add_filters(SEARCH_PROFILE_TABLE, inner_query, **filters)
        stmt = select(sa_exists(inner_query))
        result = await self.__session.execute(stmt)
        return bool(result.scalar())

    async def get_active_profiles(self) -> list[SearchProfile]:
        query = self._get_query(SearchProfile)
        query = self._add_filters(SEARCH_PROFILE_TABLE, query, is_active=True)
        result = await self.__session.execute(query)
        return list(result.scalars().all())
