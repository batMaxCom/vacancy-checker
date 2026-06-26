from dataclasses import dataclass

from user.application.common.application_error import ApplicationError, ApplicationTypeError
from user.application.common.const.errors import APPLICATION_FORBIDDEN
from user.application.common.dto import Pagination, PaginationResult, UserBriefDTO
from user.application.ports.auth import IdentityProvider, PermissionChecker
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
        identity_provider: IdentityProvider,
        permission_checker: PermissionChecker
    ) -> None:
        self.__user_gateway = user_gateway
        self.__identity_provider = identity_provider
        self.__permission_checker = permission_checker


    async def handle(self, query: GetUsersQuery) -> PaginationResult[UserBriefDTO]:
        user_role = self.__identity_provider.current_user_role()
        if not self.__permission_checker.is_admin(user_role):
            raise ApplicationError(
                type=ApplicationTypeError.FORBIDDEN,
                message=APPLICATION_FORBIDDEN
            )
        filters: dict[str, object] = {}
        if query.role is not None:
            filters["role"] = query.role
        if query.status is not None:
            filters["status"] = query.status

        return await self.__user_gateway.get_paginated(
            pagination=query.pagination,
            **filters,
        )
