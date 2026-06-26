from dataclasses import dataclass

from user.application.common.application_error import ApplicationError, ApplicationTypeError
from user.application.common.const.errors import APPLICATION_FORBIDDEN
from user.application.ports import AsyncTransactionManager, Logger, TimeProvider
from user.application.ports.auth import IdentityProvider, PermissionChecker
from user.application.ports.cqrs import Command, CommandHandler
from user.domain.user.repository import UserRepository
from user.domain.user.value_objects import UserId


@dataclass(frozen=True, slots=True)
class DeleteUserByIdCommand(Command[None]):
    user_id: UserId


class DeleteUserByIdCommandHandler(CommandHandler[DeleteUserByIdCommand, None]):
    def __init__(
        self,
        user_repository: UserRepository,
        transaction_manager: AsyncTransactionManager,
        identity_provider: IdentityProvider,
        permission_checker: PermissionChecker,
        time_provider: TimeProvider,
        logger: Logger,
    ) -> None:
        self.__user_repository = user_repository
        self.__transaction_manager = transaction_manager
        self.__identity_provider = identity_provider
        self.__permission_checker = permission_checker
        self.__time_provider = time_provider
        self.__logger = logger

    async def handle(self, command: DeleteUserByIdCommand) -> None:
        user_role = self.__identity_provider.current_user_role()
        if not self.__permission_checker.is_admin(user_role):
            raise ApplicationError(
                type=ApplicationTypeError.FORBIDDEN,
                message=APPLICATION_FORBIDDEN
            )
        user = await self.__user_repository.get(id=command.user_id)

        user.deactivate()

        await self.__user_repository.update(user)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="DELETE_USER_COMMAND",
            user_id=str(command.user_id),
        )
