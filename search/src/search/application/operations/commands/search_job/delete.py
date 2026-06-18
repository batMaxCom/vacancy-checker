from dataclasses import dataclass

from search.application.ports.cqrs import Command
from search.application.ports.cqrs.handlers import CommandHandler
from search.application.ports.transaction_manager import AsyncTransactionManager
from search.domain.search_job.repository import SearchJobRepository
from search.domain.search_job.value_objects import SearchJobId


@dataclass(frozen=True, slots=True)
class DeleteSearchJobCommand(Command[None]):
    search_job_id: SearchJobId


class DeleteSearchJobCommandHandler(CommandHandler[DeleteSearchJobCommand, None]):
    def __init__(
        self,
        search_job_repository: SearchJobRepository,
        transaction_manager: AsyncTransactionManager,
    ) -> None:
        self.__search_job_repository = search_job_repository
        self.__transaction_manager = transaction_manager

    async def handle(self, command: DeleteSearchJobCommand) -> None:
        search_job = await self.__search_job_repository.get(
            search_job_id=command.search_job_id,
        )

        await self.__search_job_repository.delete(search_job)
        await self.__transaction_manager.commit()
