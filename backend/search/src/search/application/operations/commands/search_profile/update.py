from dataclasses import dataclass

from search.application.ports.cqrs import Command
from search.application.ports.cqrs.handlers import CommandHandler
from search.application.ports.transaction_manager import AsyncTransactionManager
from search.domain.search_profile.repository import SearchProfileRepository
from search.domain.search_profile.value_objects import (
    Keyword,
    SearchInterval,
    SearchProfileId,
)


@dataclass(frozen=True, slots=True)
class UpdateSearchProfileCommand(Command[None]):
    search_profile_id: SearchProfileId
    name: str
    keywords: list[str]
    search_interval_minutes: int


class UpdateSearchProfileCommandHandler(CommandHandler[UpdateSearchProfileCommand, None]):
    def __init__(
        self,
        search_profile_repository: SearchProfileRepository,
        transaction_manager: AsyncTransactionManager,
    ) -> None:
        self.__search_profile_repository = search_profile_repository
        self.__transaction_manager = transaction_manager

    async def handle(self, command: UpdateSearchProfileCommand) -> None:
        search_profile = await self.__search_profile_repository.get(
            id=command.search_profile_id,
        )
        search_profile.update_profile(
            name=command.name,
            keywords=[Keyword(k) for k in command.keywords],
            search_interval=SearchInterval(minutes=command.search_interval_minutes),
        )

        await self.__search_profile_repository.update(search_profile)
        await self.__transaction_manager.commit()
