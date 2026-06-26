from dataclasses import dataclass

from search.application.common.dto import SearchProfileDto
from search.application.ports.auth import IdentityProvider
from search.application.ports.cqrs import Query
from search.application.ports.cqrs.handlers import QueryHandler
from search.application.ports.gateways import SearchProfileGateway


@dataclass(frozen=True, slots=True)
class GetUserSearchProfilesQuery(Query[list[SearchProfileDto]]):
    ...


class GetUserSearchProfilesQueryHandler(
    QueryHandler[GetUserSearchProfilesQuery, list[SearchProfileDto]],
):
    def __init__(
        self,
        search_profile_gateway: SearchProfileGateway,
        identity_provider: IdentityProvider
    ) -> None:
        self.__search_profile_gateway = search_profile_gateway
        self.__identity_provider = identity_provider

    async def handle(self, query: GetUserSearchProfilesQuery) -> list[SearchProfileDto]:
        user_id = self.__identity_provider.current_user_id()
        return await self.__search_profile_gateway.get_by_user_id(
            user_id=user_id
        )
