from dataclasses import dataclass

from vacancy.application.ports import AsyncTransactionManager, TimeProvider
from vacancy.application.ports.cqrs import Command, CommandHandler
from vacancy.domain.sources.repository import SourceRepository
from vacancy.domain.sources.value_objects import SourceId


@dataclass(frozen=True, slots=True)
class UpdateSourceCommand(Command[None]):
    source_id: SourceId
    name: str | None = None
    base_url: str | None = None
    is_active: bool | None = None


class UpdateSourceCommandHandler(CommandHandler[UpdateSourceCommand, None]):
    def __init__(
        self,
        source_repository: SourceRepository,
        transaction_manager: AsyncTransactionManager,
        time_provider: TimeProvider,
    ) -> None:
        self.__source_repository = source_repository
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider

    async def handle(self, command: UpdateSourceCommand) -> None:
        source = await self.__source_repository.get(source_id=command.source_id)

        if command.name is not None:
            source.rename(command.name)
        if command.base_url is not None:
            source.set_base_url(command.base_url)
        if command.is_active is not None:
            if command.is_active:
                source.activate()
            else:
                source.deactivate()

        await self.__source_repository.update(source)
        await self.__transaction_manager.commit()
