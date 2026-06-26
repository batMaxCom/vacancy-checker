from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.credential.entity import UserCredential
from auth.domain.credential.repository import CredentialRepository
from auth.infrastructure.persistence.adapters.common.mixins import FilterMixin, QueryMixin
from auth.infrastructure.persistence.adapters.common.utils import unwrap_filters
from auth.infrastructure.persistence.tables import CREDENTIAL_TABLE


class CredentialRepositoryImpl(CredentialRepository, QueryMixin, FilterMixin):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, entity: UserCredential) -> None:
        self.__session.add(entity)

    async def update(self, entity: UserCredential) -> None:
        await self.__session.merge(entity)

    async def get(self, **filters: Any) -> UserCredential | None:
        query = self._get_query(UserCredential)
        query = self._add_filters(CREDENTIAL_TABLE, query, **unwrap_filters(**filters))
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, entity: UserCredential) -> None:
        await self.__session.delete(entity)

    async def exists(self, **filters: Any) -> bool:
        query = self._get_query(CREDENTIAL_TABLE, ["user_id"])
        query = self._add_filters(CREDENTIAL_TABLE, query, **unwrap_filters(**filters))
        result = await self.__session.execute(query)
        return result.scalar() is not None
