from dataclasses import dataclass

from user.application.ports import AsyncTransactionManager, Logger, TimeProvider
from user.application.ports.cqrs import Command, CommandHandler
from user.domain.user.repository import UserRepository
from user.domain.user.value_objects import UserId, UserRole


@dataclass(frozen=True, slots=True)
class ChangeRoleCommand(Command[None]):
    user_id: UserId
    role: UserRole


class ChangeRoleCommandHandler(CommandHandler[ChangeRoleCommand, None]):
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

    async def handle(self, command: ChangeRoleCommand) -> None:
        user = await self.__user_repository.get(id=command.user_id)

        user.change_role(command.role)

        await self.__user_repository.update(user)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="CHANGE_ROLE_COMMAND",
            user_id=str(command.user_id),
            role=command.role.name,
        )
