from dataclasses import dataclass

from vacancy.application.ports import AsyncTransactionManager, TimeProvider, UUIDGenerator
from vacancy.application.ports.cqrs import Command, CommandHandler
from vacancy.domain.sources.entity import Source
from vacancy.domain.sources.repository import SourceRepository
from vacancy.domain.sources.value_objects import SourceId


@dataclass(frozen=True, slots=True)
class CreateSourceCommand(Command[None]):
    name: str
    base_url: str = ""


class CreateSourceCommandHandler(CommandHandler[CreateSourceCommand, None]):
    def __init__(
        self,
        id_generator: UUIDGenerator,
        source_repository: SourceRepository,
        transaction_manager: AsyncTransactionManager,
        time_provider: TimeProvider,
    ) -> None:
        self.__id_generator = id_generator
        self.__source_repository = source_repository
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider

    async def handle(self, command: CreateSourceCommand) -> None:
        source = Source.create(
            source_id=SourceId(self.__id_generator.next_id()),
            name=command.name,
            base_url=command.base_url,
        )

        await self.__source_repository.add(source)
        await self.__transaction_manager.commit()
