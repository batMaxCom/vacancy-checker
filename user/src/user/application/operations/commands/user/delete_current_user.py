from dataclasses import dataclass

from user.application.ports import AsyncTransactionManager, Logger, TimeProvider
from user.application.ports.auth import IdentityProvider
from user.application.ports.cqrs import Command, CommandHandler
from user.domain.user.repository import UserRepository


@dataclass(frozen=True, slots=True)
class DeleteUserCommand(Command[None]):
    ...

class DeleteUserCommandHandler(CommandHandler[DeleteUserCommand, None]):
    def __init__(
        self,
        user_repository: UserRepository,
        transaction_manager: AsyncTransactionManager,
        identity_provider: IdentityProvider,
        time_provider: TimeProvider,
        logger: Logger,
    ) -> None:
        self.__user_repository = user_repository
        self.__transaction_manager = transaction_manager
        self.__identity_provider = identity_provider
        self.__time_provider = time_provider
        self.__logger = logger

    async def handle(self, command: DeleteUserCommand) -> None:
        user_id = self.__identity_provider.current_user_id()
        user = await self.__user_repository.get(id=user_id)
        user.deactivate()

        await self.__user_repository.update(user)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="DELETE_USER_COMMAND",
            user_id=str(user_id),
        )
