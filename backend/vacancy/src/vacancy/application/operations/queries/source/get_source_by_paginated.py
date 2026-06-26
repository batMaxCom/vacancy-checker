from dataclasses import dataclass
from typing import Any

from vacancy.application.common.dto import PaginationDto, PaginationResultDto, SourceDto
from vacancy.application.ports.cqrs import Query, QueryHandler
from vacancy.application.ports.gateways import SourceGateway


@dataclass(frozen=True, slots=True)
class GetSourceByPaginatedQuery(Query[PaginationResultDto[SourceDto]]):
    pagination: PaginationDto
    filters: dict[str, Any] | None = None


class GetSourceByPaginatedQueryHandler(
    QueryHandler[GetSourceByPaginatedQuery,
    PaginationResultDto[SourceDto]]
):
    def __init__(
        self,
        source_gateway: SourceGateway,
    ) -> None:
        self.__source_gateway = source_gateway

    async def handle(self, query: GetSourceByPaginatedQuery) -> PaginationResultDto[SourceDto]:
        return await self.__source_gateway.get_paginated(
            pagination=query.pagination,
            **(query.filters or {}),
        )
