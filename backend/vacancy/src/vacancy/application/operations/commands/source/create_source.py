from dataclasses import dataclass

from vacancy.application.ports import AsyncTransactionManager, TimeProvider, UUIDGenerator
from vacancy.application.ports.cqrs import Command, CommandHandler
from vacancy.application.ports.logger import CQRSLogger
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
        logger: CQRSLogger,
    ) -> None:
        self.__id_generator = id_generator
        self.__source_repository = source_repository
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider
        self.__logger = logger

    async def handle(self, command: CreateSourceCommand) -> None:
        source_id = SourceId(self.__id_generator.next_id())

        source = Source.create(
            source_id=source_id,
            name=command.name,
            base_url=command.base_url,
        )

        await self.__source_repository.add(source)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="CREATE_SOURCE_COMMAND",
            source_id=str(source_id),
            name=command.name,
            base_url=command.base_url,
        )
