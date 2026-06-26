from dataclasses import dataclass

from search.application.common.dto import SearchProfileDto
from search.application.ports.cqrs import Query
from search.application.ports.cqrs.handlers import QueryHandler
from search.application.ports.gateways import SearchProfileGateway
from search.domain.search_profile.value_objects import SearchProfileId


@dataclass(frozen=True, slots=True)
class GetSearchProfileQuery(Query[SearchProfileDto | None]):
    search_profile_id: SearchProfileId


class GetSearchProfileQueryHandler(QueryHandler[GetSearchProfileQuery, SearchProfileDto | None]):
    def __init__(
        self,
        search_profile_gateway: SearchProfileGateway,
    ) -> None:
        self.__search_profile_gateway = search_profile_gateway

    async def handle(self, query: GetSearchProfileQuery) -> SearchProfileDto | None:
        return await self.__search_profile_gateway.get_by_id(
            search_profile_id=query.search_profile_id,
        )
