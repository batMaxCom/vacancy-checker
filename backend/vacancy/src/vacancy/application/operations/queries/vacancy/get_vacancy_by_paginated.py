from dataclasses import dataclass
from typing import Any

from vacancy.application.common.dto import PaginationDto, PaginationResultDto, VacancyDto
from vacancy.application.ports.cqrs import Query, QueryHandler
from vacancy.application.ports.gateways import VacancyGateway


@dataclass(frozen=True, slots=True)
class GetVacancyByPaginatedQuery(Query[PaginationResultDto[VacancyDto]]):
    pagination: PaginationDto
    filters: dict[str, Any] | None = None


class GetVacancyByPaginatedQueryHandler(
    QueryHandler[GetVacancyByPaginatedQuery, PaginationResultDto[VacancyDto]]
):
    def __init__(
        self,
        vacancy_gateway: VacancyGateway,
    ) -> None:
        self.__vacancy_gateway = vacancy_gateway

    async def handle(self, query: GetVacancyByPaginatedQuery) -> PaginationResultDto[VacancyDto]:
        return await self.__vacancy_gateway.get_paginated(
            pagination=query.pagination,
            **(query.filters or {}),
        )
