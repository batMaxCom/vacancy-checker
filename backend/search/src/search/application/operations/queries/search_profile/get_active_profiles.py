from dataclasses import dataclass

from search.application.common.dto import SearchProfileDto
from search.application.ports.cqrs import Query
from search.application.ports.cqrs.handlers import QueryHandler
from search.application.ports.gateways import SearchProfileGateway


@dataclass(frozen=True, slots=True)
class GetActiveProfilesQuery(Query[list[SearchProfileDto]]):
    pass


class GetActiveProfilesQueryHandler(QueryHandler[GetActiveProfilesQuery, list[SearchProfileDto]]):
    def __init__(
        self,
        search_profile_gateway: SearchProfileGateway,
    ) -> None:
        self.__search_profile_gateway = search_profile_gateway

    async def handle(self, query: GetActiveProfilesQuery) -> list[SearchProfileDto]:
        return await self.__search_profile_gateway.get_active_profiles()
