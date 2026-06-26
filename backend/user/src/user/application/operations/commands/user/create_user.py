from dataclasses import dataclass

from user.application.ports import AsyncTransactionManager, Logger, TimeProvider
from user.application.ports.cqrs import Command, CommandHandler
from user.domain.user.entity import User
from user.domain.user.repository import UserRepository
from user.domain.user.value_objects import Email, FirstName, LastName, UserId, UserRole, UserStatus


@dataclass(frozen=True, slots=True)
class CreateUserCommand(Command[None]):
    user_id: UserId
    email: Email
    first_name: FirstName
    last_name: LastName


class CreateUserCommandHandler(CommandHandler[CreateUserCommand, None]):
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

    async def handle(self, command: CreateUserCommand) -> None:
        now = self.__time_provider.current_time()

        user = User(
            user_id=command.user_id,
            email=command.email,
            first_name=command.first_name,
            last_name=command.last_name,
            role=UserRole.USER,
            status=UserStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )

        await self.__user_repository.add(user)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="CREATE_USER_COMMAND",
            user_id=str(command.user_id),
            email=str(command.email.value),
        )
