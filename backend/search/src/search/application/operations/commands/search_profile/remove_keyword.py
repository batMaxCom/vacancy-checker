from dataclasses import dataclass

from search.application.ports.cqrs import Command
from search.application.ports.cqrs.handlers import CommandHandler
from search.application.ports.transaction_manager import AsyncTransactionManager
from search.domain.search_profile.repository import SearchProfileRepository
from search.domain.search_profile.value_objects import SearchProfileId


@dataclass(frozen=True, slots=True)
class RemoveKeywordCommand(Command[None]):
    search_profile_id: SearchProfileId
    keyword: str


class RemoveKeywordCommandHandler(CommandHandler[RemoveKeywordCommand, None]):
    def __init__(
        self,
        search_profile_repository: SearchProfileRepository,
        transaction_manager: AsyncTransactionManager,
    ) -> None:
        self.__search_profile_repository = search_profile_repository
        self.__transaction_manager = transaction_manager

    async def handle(self, command: RemoveKeywordCommand) -> None:
        search_profile = await self.__search_profile_repository.get(
            search_profile_id=command.search_profile_id,
        )
        search_profile.remove_keyword(command.keyword)

        await self.__search_profile_repository.update(search_profile)
        await self.__transaction_manager.commit()
