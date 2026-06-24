from dataclasses import dataclass

from user.application.ports import AsyncTransactionManager, Logger, TimeProvider
from user.application.ports.cqrs import Command, CommandHandler
from user.domain.user.repository import UserRepository
from user.domain.user.value_objects import UserId


@dataclass(frozen=True, slots=True)
class ActivateUserCommand(Command[None]):
    user_id: UserId


class ActivateUserCommandHandler(CommandHandler[ActivateUserCommand, None]):
    def __init__(
        self,
        user_repository: UserRepository,
        transaction_manager: AsyncTransactionManager,
        time_provider: TimeProvider,
        logger: Logger,
    ) -> None:
        self.__user_repository = user_repository
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider
        self.__logger = logger

    async def handle(self, command: ActivateUserCommand) -> None:
        user = await self.__user_repository.get(id=command.user_id)

        user.activate()

        await self.__user_repository.update(user)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="ACTIVATE_USER_COMMAND",
            user_id=str(command.user_id),
        )
