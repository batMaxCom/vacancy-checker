from dataclasses import dataclass

from search.application.ports.cqrs import Command
from search.application.ports.cqrs.handlers import CommandHandler
from search.application.ports.id_generator import UUIDGenerator
from search.application.ports.time_provider import TimeProvider
from search.application.ports.transaction_manager import AsyncTransactionManager
from search.domain.common.value_objects import UserId
from search.domain.search_profile.entity import SearchProfile
from search.domain.search_profile.repository import SearchProfileRepository
from search.domain.search_profile.value_objects import (
    Keyword,
    SearchInterval,
    SearchProfileId,
)


@dataclass(frozen=True, slots=True)
class CreateSearchProfileCommand(Command[SearchProfileId]):
    user_id: UserId
    name: str
    keywords: list[str]
    search_interval_minutes: int


class CreateSearchProfileCommandHandler(
    CommandHandler[CreateSearchProfileCommand, SearchProfileId],
):
    def __init__(
        self,
        id_generator: UUIDGenerator,
        search_profile_repository: SearchProfileRepository,
        transaction_manager: AsyncTransactionManager,
        time_provider: TimeProvider,
    ) -> None:
        self.__id_generator = id_generator
        self.__search_profile_repository = search_profile_repository
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider

    async def handle(self, command: CreateSearchProfileCommand) -> SearchProfileId:
        now = self.__time_provider.current_time()
        search_profile = SearchProfile(
            search_profile_id=SearchProfileId(self.__id_generator.next_id()),
            user_id=command.user_id,
            name=command.name,
            keywords=[Keyword(k) for k in command.keywords],
            search_interval=SearchInterval(minutes=command.search_interval_minutes),
            created_at=now,
            updated_at=now,
        )

        await self.__search_profile_repository.add(search_profile)
        await self.__transaction_manager.commit()

        return search_profile.entity_id
