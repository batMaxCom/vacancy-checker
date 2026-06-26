from dataclasses import dataclass

from vacancy.application.ports import AsyncTransactionManager
from vacancy.application.ports.cqrs import Command, CommandHandler
from vacancy.application.ports.logger import CQRSLogger
from vacancy.domain.vacancies.repository import VacancyRepository
from vacancy.domain.vacancies.value_objects import ProfileId


@dataclass(frozen=True, slots=True)
class DeleteVacancyByProfileIdCommand(Command[None]):
    profile_id: ProfileId


class DeleteVacancyByProfileIdCommandHandler(CommandHandler[DeleteVacancyByProfileIdCommand, None]):
    def __init__(
        self,
        vacancy_repository: VacancyRepository,
        transaction_manager: AsyncTransactionManager,
        logger: CQRSLogger,
    ) -> None:
        self.__vacancy_repository = vacancy_repository
        self.__transaction_manager = transaction_manager
        self.__logger = logger

    async def handle(self, command: DeleteVacancyByProfileIdCommand) -> None:
        await self.__vacancy_repository.delete_by_profile_id(command.profile_id)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="DELETE_VACANCY_BY_PROFILE_ID_COMMAND",
            profile_id=str(command.profile_id),
        )
