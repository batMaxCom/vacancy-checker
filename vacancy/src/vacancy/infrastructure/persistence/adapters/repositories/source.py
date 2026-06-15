from typing import Any, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vacancy.domain.sources.entity import Source
from vacancy.domain.sources.repository import SourceRepository
from vacancy.infrastructure.persistence.adapters.common.mixins import FilterMixin, QueryMixin
from vacancy.infrastructure.persistence.tables.source import SOURCE_TABLE


class SourceRepositoryImpl(SourceRepository, QueryMixin, FilterMixin):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, entity: Source) -> None:
        self.__session.add(entity)

    async def update(self, entity: Source) -> None:
        await self.__session.merge(entity)

    async def get(self, **filters: Any) -> Source:
        query = self._get_query(SOURCE_TABLE)
        query = self._add_filters(SOURCE_TABLE, query, **filters)
        result = await self.__session.execute(query)
        return cast("Source", result.scalar_one())

    async def delete(self, entity: Source) -> None:
        await self.__session.delete(entity)

    async def exists(self, **filters: Any) -> bool:
        query = select(SOURCE_TABLE.c.id)
        query = self._add_filters(SOURCE_TABLE, query, **filters)
        result = await self.__session.execute(query)
        return result.scalar() is not None
