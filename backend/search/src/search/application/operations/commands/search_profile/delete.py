from dataclasses import dataclass

from search.application.ports.cqrs import Command
from search.application.ports.cqrs.handlers import CommandHandler
from search.application.ports.transaction_manager import AsyncTransactionManager
from search.domain.search_job.repository import SearchJobRepository
from search.domain.search_profile.repository import SearchProfileRepository
from search.domain.search_profile.value_objects import SearchProfileId


@dataclass(frozen=True, slots=True)
class DeleteSearchProfileCommand(Command[None]):
    search_profile_id: SearchProfileId


class DeleteSearchProfileCommandHandler(CommandHandler[DeleteSearchProfileCommand, None]):
    def __init__(
        self,
        search_profile_repository: SearchProfileRepository,
        search_job_repository: SearchJobRepository,
        transaction_manager: AsyncTransactionManager,
    ) -> None:
        self.__search_profile_repository = search_profile_repository
        self.__search_job_repository = search_job_repository
        self.__transaction_manager = transaction_manager

    async def handle(self, command: DeleteSearchProfileCommand) -> None:
        search_profile = await self.__search_profile_repository.get(
            id=command.search_profile_id,
        )

        search_jobs = await self.__search_job_repository.get_all_by_profile_id(
            profile_id=command.search_profile_id,
        )

        for search_job in search_jobs:
            await self.__search_job_repository.delete(search_job)

        await self.__search_profile_repository.delete(search_profile)
        await self.__transaction_manager.commit()
