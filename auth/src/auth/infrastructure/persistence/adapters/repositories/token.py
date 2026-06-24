from typing import Any, cast

from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.token.entity import RefreshToken
from auth.domain.token.repository import TokenRepository
from auth.infrastructure.persistence.adapters.common.mixins import FilterMixin, QueryMixin
from auth.infrastructure.persistence.adapters.common.utils import unwrap_filters
from auth.infrastructure.persistence.tables import TOKEN_TABLE


class TokenRepositoryImpl(TokenRepository, QueryMixin, FilterMixin):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, entity: RefreshToken) -> None:
        self.__session.add(entity)

    async def update(self, entity: RefreshToken) -> None:
        await self.__session.merge(entity)

    async def get(self, **filters: Any) -> RefreshToken:
        query = self._get_query(RefreshToken)
        query = self._add_filters(TOKEN_TABLE, query, **unwrap_filters(**filters))
        result = await self.__session.execute(query)
        return cast("RefreshToken", result.scalar_one())

    async def delete(self, entity: RefreshToken) -> None:
        await self.__session.delete(entity)

    async def get_all(self, **filters: Any) -> list[RefreshToken]:
        query = self._get_query(RefreshToken)
        query = self._add_filters(TOKEN_TABLE, query, **unwrap_filters(**filters))
        result = await self.__session.execute(query)
        return list(result.scalars().all())

    async def exists(self, **filters: Any) -> bool:
        query = self._get_query(TOKEN_TABLE, ["token_id"])
        query = self._add_filters(TOKEN_TABLE, query, **unwrap_filters(**filters))
        result = await self.__session.execute(query)
        return result.scalar() is not None
