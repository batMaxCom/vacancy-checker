from typing import Any, cast

from sqlalchemy.ext.asyncio import AsyncSession

from user.domain.user.entity import User
from user.domain.user.repository import UserRepository
from user.infrastructure.persistence.adapters.common.mixins import FilterMixin, QueryMixin
from user.infrastructure.persistence.tables import USER_TABLE


class UserRepositoryImpl(UserRepository, QueryMixin, FilterMixin):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, entity: User) -> None:
        self.__session.add(entity)

    async def update(self, entity: User) -> None:
        await self.__session.merge(entity)

    async def get(self, **filters: Any) -> User:
        query = self._get_query(User)
        query = self._add_filters(USER_TABLE, query, **filters)
        result = await self.__session.execute(query)
        return cast("User", result.scalar_one())

    async def delete(self, entity: User) -> None:
        await self.__session.delete(entity)

    async def exists(self, **filters: Any) -> bool:
        query = self._get_query(USER_TABLE, ["id"])
        query = self._add_filters(USER_TABLE, query, **filters)
        result = await self.__session.execute(query)
        return result.scalar() is not None

    async def get_all(self, **filters: Any) -> list[User]:
        query = self._get_query(User)
        query = self._add_filters(USER_TABLE, query, **filters)
        result = await self.__session.execute(query)
        return list(result.scalars().all())
