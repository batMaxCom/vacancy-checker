from dataclasses import dataclass

from user.application.common.dto import Pagination, PaginationResult, UserBriefDTO
from user.application.ports.cqrs import Query, QueryHandler
from user.application.ports.gateways.user import UserGateway


@dataclass(frozen=True, slots=True)
class GetUsersQuery(Query[PaginationResult[UserBriefDTO]]):
    pagination: Pagination
    role: str | None = None
    status: str | None = None


class GetUsersQueryHandler(QueryHandler[GetUsersQuery, PaginationResult[UserBriefDTO]]):
    def __init__(
        self,
        user_gateway: UserGateway,
    ) -> None:
        self.__user_gateway = user_gateway

    async def handle(self, query: GetUsersQuery) -> PaginationResult[UserBriefDTO]:
        filters: dict[str, object] = {}
        if query.role is not None:
            filters["role"] = query.role
        if query.status is not None:
            filters["status"] = query.status

        return await self.__user_gateway.get_paginated(
            pagination=query.pagination,
            **filters,
        )
