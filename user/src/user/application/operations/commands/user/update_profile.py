from dataclasses import dataclass

from user.application.ports import AsyncTransactionManager, Logger, TimeProvider
from user.application.ports.cqrs import Command, CommandHandler
from user.domain.user.repository import UserRepository
from user.domain.user.value_objects import AvatarUrl, FirstName, LastName, UserId


@dataclass(frozen=True, slots=True)
class UpdateProfileCommand(Command[None]):
    user_id: UserId
    first_name: FirstName
    last_name: LastName
    avatar_url: AvatarUrl | None = None


class UpdateProfileCommandHandler(CommandHandler[UpdateProfileCommand, None]):
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

    async def handle(self, command: UpdateProfileCommand) -> None:
        user = await self.__user_repository.get(id=command.user_id)

        user.update_profile(
            first_name=command.first_name,
            last_name=command.last_name,
            avatar_url=command.avatar_url,
        )

        await self.__user_repository.update(user)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="UPDATE_PROFILE_COMMAND",
            user_id=str(command.user_id),
        )
