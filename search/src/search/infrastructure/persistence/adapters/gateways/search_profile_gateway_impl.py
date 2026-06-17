from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from search.application.common.dto.search_profile_dto import KeywordDto, SearchProfileDto
from search.application.ports.gateways import SearchProfileGateway
from search.domain.common.value_objects import UserId
from search.domain.search_profile.value_objects import Keyword, SearchProfileId
from search.infrastructure.persistence.adapters.common.mixins import FilterMixin, QueryMixin
from search.infrastructure.persistence.tables import SEARCH_PROFILE_TABLE


class SearchProfileGatewayImpl(QueryMixin, FilterMixin, SearchProfileGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def get_by_id(self, search_profile_id: SearchProfileId) -> SearchProfileDto | None:
        query = self._get_query(SEARCH_PROFILE_TABLE)
        query = self._add_filters(SEARCH_PROFILE_TABLE, query, id=search_profile_id)
        result = await self.__session.execute(query)
        row = result.one_or_none()
        if not row:
            return None
        return self.__map_row(row)

    async def get_by_user_id(self, user_id: UserId) -> list[SearchProfileDto]:
        query = self._get_query(SEARCH_PROFILE_TABLE)
        query = self._add_filters(SEARCH_PROFILE_TABLE, query, user_id=user_id)
        result = await self.__session.execute(query)
        rows = result.all()
        return [self.__map_row(row) for row in rows]

    async def get_active_profiles(self) -> list[SearchProfileDto]:
        query = self._get_query(SEARCH_PROFILE_TABLE)
        query = self._add_filters(SEARCH_PROFILE_TABLE, query, is_active=True)
        result = await self.__session.execute(query)
        rows = result.all()
        return [self.__map_row(row) for row in rows]

    @staticmethod
    def __map_row(row: Any) -> SearchProfileDto:
        keywords = [
            KeywordDto(value=k.value) if isinstance(k, Keyword) else KeywordDto(value=k)
            for k in (row.keywords or [])
        ]
        return SearchProfileDto(
            id=SearchProfileId(row.id),
            user_id=UserId(row.user_id),
            name=row.name,
            keywords=keywords,
            search_interval_minutes=row.search_interval_minutes,
            is_active=row.is_active,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
