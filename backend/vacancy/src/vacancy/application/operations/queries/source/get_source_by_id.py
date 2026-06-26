from dataclasses import dataclass

from vacancy.application.common.dto import SourceDto
from vacancy.application.ports.cqrs import Query, QueryHandler
from vacancy.application.ports.gateways import SourceGateway
from vacancy.domain.sources.value_objects import SourceId


@dataclass(frozen=True, slots=True)
class GetSourceByIdQuery(Query[SourceDto | None]):
    source_id: SourceId


class GetSourceByIdQueryHandler(QueryHandler[GetSourceByIdQuery, SourceDto | None]):
    def __init__(
        self,
        source_gateway: SourceGateway,
    ) -> None:
        self.__source_gateway = source_gateway

    async def handle(self, query: GetSourceByIdQuery) -> SourceDto | None:
        return await self.__source_gateway.get_by_id(source_id=query.source_id)
