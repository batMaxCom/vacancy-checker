from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from vacancy.application.ports import AsyncTransactionManager, TimeProvider
from vacancy.application.ports.cqrs import Command, CommandHandler
from vacancy.application.ports.logger import CQRSLogger
from vacancy.domain.sources.entity import Source
from vacancy.domain.sources.repository import SourceRepository
from vacancy.domain.sources.value_objects import SourceId
from vacancy.domain.vacancies.entity import Vacancy
from vacancy.domain.vacancies.enums import EmploymentType, WorkFormat
from vacancy.domain.vacancies.repository import VacancyRepository
from vacancy.domain.vacancies.value_objects import ProfileId, Salary, VacancyId


@dataclass(frozen=True, slots=True)
class CreateVacancyCommand(Command[None]):
    vacancy_id: VacancyId
    profile_id: ProfileId
    external_id: str | None
    title: str
    description: str
    company_name: str
    employment_type: EmploymentType | None
    work_format: WorkFormat | None
    salary: Salary | None
    location: str | None
    url: str
    published_at: datetime | None
    source: str
    source_url: str


class CreateVacancyCommandHandler(CommandHandler[CreateVacancyCommand, None]):
    def __init__(
        self,
        vacancy_repository: VacancyRepository,
        source_repository: SourceRepository,
        transaction_manager: AsyncTransactionManager,
        time_provider: TimeProvider,
        logger: CQRSLogger,
    ) -> None:
        self.__vacancy_repository = vacancy_repository
        self.__source_repository = source_repository
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider
        self.__logger = logger

    async def handle(self, command: CreateVacancyCommand) -> None:
        source = await self.__source_repository.get(name=command.source)
        if source is None:
            source = Source.create(
                source_id=SourceId(uuid4()),
                name=command.source,
                base_url=command.source_url,
            )
            await self.__source_repository.add(source)
            await self.__transaction_manager.flush()
        if await self.__vacancy_repository.exists(external_id=command.external_id):
            return
        vacancy = Vacancy.create(
            vacancy_id=command.vacancy_id,
            source_id=source.entity_id,
            profile_id=command.profile_id,
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

        await self.__logger.ainfo(
            event="CREATE_VACANCY_COMMAND",
            vacancy_id=str(command.vacancy_id),
            source_id=str(source.entity_id),
            external_id=command.external_id,
            title=command.title,
            company_name=command.company_name,
            url=command.url,
        )
