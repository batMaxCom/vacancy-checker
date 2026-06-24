from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from user.application.common.dto import Pagination, PaginationResult, UserBriefDTO
from user.application.ports.gateways.user import UserGateway
from user.infrastructure.persistence.adapters.common.mixins import FilterMixin, PaginationMixin
from user.infrastructure.persistence.tables import USER_TABLE


class UserGatewayImpl(UserGateway, FilterMixin, PaginationMixin):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def get_paginated(
        self,
        pagination: Pagination,
        **filters: Any,
    ) -> PaginationResult[UserBriefDTO]:
        base_query = select(
            USER_TABLE.c.id,
            USER_TABLE.c.email,
            USER_TABLE.c.first_name,
            USER_TABLE.c.last_name,
        )
        base_query = self._add_filters(USER_TABLE, base_query, **filters)

        count_query = select(func.count()).select_from(USER_TABLE)
        count_query = self._add_filters(USER_TABLE, count_query, **filters)
        count_result = await self.__session.execute(count_query)
        count_records = count_result.scalar() or 0

        base_query = self._add_query_offset_and_limit(
            base_query, pagination.page_number, pagination.page_size,
        )
        base_query = base_query.order_by(USER_TABLE.c.created_at.desc())
        result = await self.__session.execute(base_query)
        rows = result.all()

        records = [
            UserBriefDTO(
                id=str(row.id),
                email=row.email,
                first_name=row.first_name,
                last_name=row.last_name,
            )
            for row in rows
        ]

        return self._get_pagination_result(pagination, records, count_records)
