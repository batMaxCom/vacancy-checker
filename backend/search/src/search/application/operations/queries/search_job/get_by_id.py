from dataclasses import dataclass

from search.application.common.dto.search_job_dto import SearchJobDto
from search.application.ports.cqrs import Query
from search.application.ports.cqrs.handlers import QueryHandler
from search.application.ports.gateways.search_job_gateway import SearchJobGateway
from search.domain.search_job.value_objects import SearchJobId


@dataclass(frozen=True, slots=True)
class GetSearchJobQuery(Query[SearchJobDto | None]):
    search_job_id: SearchJobId


class GetSearchJobQueryHandler(QueryHandler[GetSearchJobQuery, SearchJobDto | None]):
    def __init__(
        self,
        search_job_gateway: SearchJobGateway,
    ) -> None:
        self.__search_job_gateway = search_job_gateway

    async def handle(self, query: GetSearchJobQuery) -> SearchJobDto | None:
        return await self.__search_job_gateway.get_by_id(
            search_job_id=query.search_job_id,
        )
