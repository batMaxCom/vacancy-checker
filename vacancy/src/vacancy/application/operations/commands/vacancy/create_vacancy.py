from dataclasses import dataclass
from datetime import datetime

from vacancy.application.ports import AsyncTransactionManager, TimeProvider
from vacancy.application.ports.cqrs import Command, CommandHandler
from vacancy.domain.sources.value_objects import SourceId
from vacancy.domain.vacancies.entity import Vacancy
from vacancy.domain.vacancies.enums import EmploymentType, WorkFormat
from vacancy.domain.vacancies.repository import VacancyRepository
from vacancy.domain.vacancies.value_objects import Salary, VacancyId


@dataclass(frozen=True, slots=True)
class CreateVacancyCommand(Command[None]):
    vacancy_id: VacancyId
    source_id: SourceId
    external_id: str
    title: str
    description: str
    company_name: str | None
    employment_type: EmploymentType
    work_format: WorkFormat
    salary: Salary | None
    location: str | None
    url: str
    published_at: datetime


class CreateVacancyCommandHandler(CommandHandler[CreateVacancyCommand, None]):
    def __init__(
        self,
        vacancy_repository: VacancyRepository,
        transaction_manager: AsyncTransactionManager,
        time_provider: TimeProvider,
    ) -> None:
        self.__vacancy_repository = vacancy_repository
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider

    async def handle(self, command: CreateVacancyCommand) -> None:
        vacancy = Vacancy.create(
            vacancy_id=command.vacancy_id,
            source_id=command.source_id,
            external_id=command.external_id,
            title=command.title,
            description=command.description,
            company_name=command.company_name,
            employment_type=command.employment_type,
            work_format=command.work_format,
            salary=command.salary,
            location=command.location,
            url=command.url,
            published_at=command.published_at,
        )

        await self.__vacancy_repository.add(vacancy)
        await self.__transaction_manager.commit()
