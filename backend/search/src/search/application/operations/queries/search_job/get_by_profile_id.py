from dataclasses import dataclass

from search.application.common.dto.search_job_dto import SearchJobDto
from search.application.ports.cqrs import Query
from search.application.ports.cqrs.handlers import QueryHandler
from search.application.ports.gateways.search_job_gateway import SearchJobGateway
from search.domain.search_profile.value_objects import SearchProfileId


@dataclass(frozen=True, slots=True)
class GetProfileJobsQuery(Query[list[SearchJobDto]]):
    profile_id: SearchProfileId


class GetProfileJobsQueryHandler(QueryHandler[GetProfileJobsQuery, list[SearchJobDto]]):
    def __init__(
        self,
        search_job_gateway: SearchJobGateway,
    ) -> None:
        self.__search_job_gateway = search_job_gateway

    async def handle(self, query: GetProfileJobsQuery) -> list[SearchJobDto]:
        return await self.__search_job_gateway.get_by_profile_id(
            profile_id=query.profile_id,
        )
