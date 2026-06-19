from dataclasses import dataclass

from search.application.common.dto import SelectSearchProfileDto
from search.application.ports.cqrs import Query
from search.application.ports.cqrs.handlers import QueryHandler
from search.application.ports.gateways import SearchProfileGateway
from search.domain.common.value_objects import UserId


@dataclass(frozen=True, slots=True)
class GetUserSearchProfilesSelectQuery(Query[list[SelectSearchProfileDto]]):
    user_id: UserId


class GetUserSearchProfilesSelectQueryHandler(
    QueryHandler[GetUserSearchProfilesSelectQuery, list[SelectSearchProfileDto]],
):
    def __init__(
        self,
        search_profile_gateway: SearchProfileGateway,
    ) -> None:
        self.__search_profile_gateway = search_profile_gateway

    async def handle(
        self,
        query: GetUserSearchProfilesSelectQuery,
    ) -> list[SelectSearchProfileDto]:
        profiles = await self.__search_profile_gateway.get_by_user_id(
            user_id=query.user_id,
        )
        return [
            SelectSearchProfileDto(id=str(p.id), name=p.name) for p in profiles
        ]
