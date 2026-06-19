from dataclasses import dataclass

from vacancy.application.ports import AsyncTransactionManager, TimeProvider
from vacancy.application.ports.cqrs import Command, CommandHandler
from vacancy.application.ports.logger import CQRSLogger
from vacancy.domain.vacancies.enums import EmploymentType, VacancyStatus, WorkFormat
from vacancy.domain.vacancies.repository import VacancyRepository
from vacancy.domain.vacancies.value_objects import Salary, VacancyId


@dataclass(frozen=True, slots=True)
class UpdateVacancyCommand(Command[None]):
    vacancy_id: VacancyId
    title: str | None = None
    description: str | None = None
    company_name: str | None = None
    employment_type: EmploymentType | None = None
    work_format: WorkFormat | None = None
    salary: Salary | None = None
    location: str | None = None
    url: str | None = None
    status: VacancyStatus | None = None


class UpdateVacancyCommandHandler(CommandHandler[UpdateVacancyCommand, None]):
    def __init__(
        self,
        vacancy_repository: VacancyRepository,
        transaction_manager: AsyncTransactionManager,
        time_provider: TimeProvider,
        logger: CQRSLogger,
    ) -> None:
        self.__vacancy_repository = vacancy_repository
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider
        self.__logger = logger

    async def handle(self, command: UpdateVacancyCommand) -> None:
        vacancy = await self.__vacancy_repository.get(id=command.vacancy_id)

        vacancy.update_details(
            title=command.title,
            description=command.description,
            company_name=command.company_name,
            employment_type=command.employment_type,
            work_format=command.work_format,
            salary=command.salary,
            location=command.location,
            url=command.url,
        )

        if command.status is VacancyStatus.ARCHIVED:
            vacancy.archive()
        elif command.status is VacancyStatus.ACTIVE:
            vacancy.activate()
        elif command.status is VacancyStatus.DELETED:
            vacancy.delete()

        await self.__vacancy_repository.update(vacancy)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="UPDATE_VACANCY_COMMAND",
            vacancy_id=str(command.vacancy_id),
            title=command.title,
            company_name=command.company_name,
            status=command.status.name if command.status else None,
            url=command.url,
        )
