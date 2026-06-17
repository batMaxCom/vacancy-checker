from dataclasses import dataclass

from search.application.common.dto import SearchProfileDto
from search.application.ports.cqrs import Query
from search.application.ports.cqrs.handlers import QueryHandler
from search.application.ports.gateways import SearchProfileGateway
from search.domain.common.value_objects import UserId


@dataclass(frozen=True, slots=True)
class GetUserSearchProfilesQuery(Query[list[SearchProfileDto]]):
    user_id: UserId


class GetUserSearchProfilesQueryHandler(
    QueryHandler[GetUserSearchProfilesQuery, list[SearchProfileDto]],
):
    def __init__(
        self,
        search_profile_gateway: SearchProfileGateway,
    ) -> None:
        self.__search_profile_gateway = search_profile_gateway

    async def handle(self, query: GetUserSearchProfilesQuery) -> list[SearchProfileDto]:
        return await self.__search_profile_gateway.get_by_user_id(
            user_id=query.user_id,
        )
