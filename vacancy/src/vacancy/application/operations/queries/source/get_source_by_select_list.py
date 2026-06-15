from dataclasses import dataclass

from vacancy.application.common.dto import SelectItemDto
from vacancy.application.ports.cqrs import Query, QueryHandler
from vacancy.application.ports.gateways import SourceGateway
from vacancy.domain.sources.value_objects import SourceId


@dataclass(frozen=True, slots=True)
class GetSourceBySelectListQuery(Query[list[SelectItemDto[SourceId]]]):
    pass


class GetSourceBySelectListQueryHandler(
    QueryHandler[GetSourceBySelectListQuery, list[SelectItemDto[SourceId]]]
):
    def __init__(
        self,
        source_gateway: SourceGateway,
    ) -> None:
        self.__source_gateway = source_gateway

    async def handle(self, query: GetSourceBySelectListQuery) -> list[SelectItemDto[SourceId]]:
        return await self.__source_gateway.get_select_list()
