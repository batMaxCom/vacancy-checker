import math
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from vacancy.application.common.dto import (
    PaginationDto,
    PaginationResultDto,
    SelectItemDto,
    SourceDto,
)
from vacancy.application.ports.gateways import SourceGateway
from vacancy.domain.sources.value_objects import SourceId
from vacancy.infrastructure.persistence.adapters.common.mixins import FilterMixin
from vacancy.infrastructure.persistence.tables.source import SOURCE_TABLE


class SourceGatewayImpl(SourceGateway, FilterMixin):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def get_by_id(self, source_id: SourceId) -> SourceDto | None:
        query = select(
            SOURCE_TABLE.c.id,
            SOURCE_TABLE.c.name,
            SOURCE_TABLE.c.base_url,
            SOURCE_TABLE.c.is_active,
        ).where(SOURCE_TABLE.c.id == source_id)

        result = await self.__session.execute(query)
        row = result.one_or_none()
        if row is None:
            return None

        return SourceDto(
            source_id=SourceId(row.id),
            name=row.name,
            base_url=row.base_url,
            is_active=row.is_active,
        )

    async def get_paginated(
        self,
        pagination: PaginationDto,
        **filters: Any,
    ) -> PaginationResultDto[SourceDto]:
        base_query = select(
            SOURCE_TABLE.c.id,
            SOURCE_TABLE.c.name,
            SOURCE_TABLE.c.base_url,
            SOURCE_TABLE.c.is_active,
        )
        base_query = self._add_filters(SOURCE_TABLE, base_query, **filters)

        count_query = select(func.count()).select_from(SOURCE_TABLE)
        count_query = self._add_filters(SOURCE_TABLE, count_query, **filters)
        count_result = await self.__session.execute(count_query)
        count_records = count_result.scalar() or 0

        page_number = pagination.page_number - 1 if pagination.page_number > 0 else 0
        base_query = base_query.offset(page_number * pagination.page_size).limit(
            pagination.page_size
        )

        result = await self.__session.execute(base_query)
        rows = result.all()

        max_page_count = math.ceil(count_records / pagination.page_size) if count_records else 0

        records = [
            SourceDto(
                source_id=SourceId(row.id),
                name=row.name,
                base_url=row.base_url,
                is_active=row.is_active,
            )
            for row in rows
        ]

        return PaginationResultDto(
            page=pagination.page_number,
            max_page_count=max_page_count,
            count_records=count_records,
            records=records,
        )

    async def get_select_list(self) -> list[SelectItemDto[SourceId]]:
        query = select(
            SOURCE_TABLE.c.id,
            SOURCE_TABLE.c.name,
        )

        result = await self.__session.execute(query)
        rows = result.all()

        return [
            SelectItemDto(
                value=SourceId(row.id),
                label=row.name,
            )
            for row in rows
        ]
