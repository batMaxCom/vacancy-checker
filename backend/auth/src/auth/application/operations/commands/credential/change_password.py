from dataclasses import dataclass

from auth.application.ports import AsyncTransactionManager, Logger, TimeProvider
from auth.application.ports.cqrs import Command, CommandHandler
from auth.application.ports.password_hasher import PasswordHasher
from auth.domain.common.value_objects import UserId
from auth.domain.credential.repository import CredentialRepository
from auth.domain.credential.value_objects import PasswordHash, PasswordSalt


@dataclass(frozen=True, slots=True)
class ChangePasswordCommand(Command[None]):
    user_id: UserId
    old_password: str
    new_password: str


class ChangePasswordCommandHandler(CommandHandler[ChangePasswordCommand, None]):
    def __init__(
        self,
        credential_repository: CredentialRepository,
        password_hasher: PasswordHasher,
        transaction_manager: AsyncTransactionManager,
        time_provider: TimeProvider,
        logger: Logger,
    ) -> None:
        self.__credential_repository = credential_repository
        self.__password_hasher = password_hasher
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider
        self.__logger = logger

    async def handle(self, command: ChangePasswordCommand) -> None:
        credential = await self.__credential_repository.get(user_id=command.user_id)

        assert credential is not None
        password_hash = self.__password_hasher.hash(command.new_password)

        credential.change_password(
            password_hash=PasswordHash(password_hash),
            password_salt=PasswordSalt(self.__password_hasher.extract_salt(password_hash)),
        )

        await self.__credential_repository.update(credential)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="CHANGE_PASSWORD_COMMAND",
            user_id=str(command.user_id),
        )
