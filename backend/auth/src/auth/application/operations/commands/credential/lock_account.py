from dataclasses import dataclass

from auth.application.ports import AsyncTransactionManager, Logger, TimeProvider
from auth.application.ports.cqrs import Command, CommandHandler
from auth.domain.common.value_objects import UserId
from auth.domain.credential.repository import CredentialRepository


@dataclass(frozen=True, slots=True)
class LockAccountCommand(Command[None]):
    user_id: UserId
    reason: str


class LockAccountCommandHandler(CommandHandler[LockAccountCommand, None]):
    def __init__(
        self,
        credential_repository: CredentialRepository,
        transaction_manager: AsyncTransactionManager,
        time_provider: TimeProvider,
        logger: Logger,
    ) -> None:
        self.__credential_repository = credential_repository
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider
        self.__logger = logger

    async def handle(self, command: LockAccountCommand) -> None:
        credential = await self.__credential_repository.get(user_id=command.user_id)

        assert credential is not None
        credential.lock(self.__time_provider.current_time())

        await self.__credential_repository.update(credential)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="LOCK_ACCOUNT_COMMAND",
            user_id=str(command.user_id),
            reason=command.reason,
        )
