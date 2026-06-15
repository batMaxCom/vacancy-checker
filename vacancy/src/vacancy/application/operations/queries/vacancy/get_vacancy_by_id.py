from dataclasses import dataclass

from vacancy.application.common.dto import VacancyDto
from vacancy.application.ports.cqrs import Query, QueryHandler
from vacancy.application.ports.gateways import VacancyGateway
from vacancy.domain.vacancies.value_objects import VacancyId


@dataclass(frozen=True, slots=True)
class GetVacancyByIdQuery(Query[VacancyDto | None]):
    vacancy_id: VacancyId


class GetVacancyByIdQueryHandler(QueryHandler[GetVacancyByIdQuery, VacancyDto | None]):
    def __init__(
        self,
        vacancy_gateway: VacancyGateway,
    ) -> None:
        self.__vacancy_gateway = vacancy_gateway

    async def handle(self, query: GetVacancyByIdQuery) -> VacancyDto | None:
        return await self.__vacancy_gateway.get_by_id(vacancy_id=query.vacancy_id)
