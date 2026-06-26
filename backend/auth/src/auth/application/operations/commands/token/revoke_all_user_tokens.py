from dataclasses import dataclass

from auth.application.ports import AsyncTransactionManager, Logger, TimeProvider
from auth.application.ports.cqrs import Command, CommandHandler
from auth.domain.common.value_objects import UserId
from auth.domain.token.repository import TokenRepository


@dataclass(frozen=True, slots=True)
class RevokeAllUserTokensCommand(Command[None]):
    user_id: UserId


class RevokeAllUserTokensCommandHandler(CommandHandler[RevokeAllUserTokensCommand, None]):
    def __init__(
        self,
        token_repository: TokenRepository,
        transaction_manager: AsyncTransactionManager,
        time_provider: TimeProvider,
        logger: Logger,
    ) -> None:
        self.__token_repository = token_repository
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider
        self.__logger = logger

    async def handle(self, command: RevokeAllUserTokensCommand) -> None:
        tokens = await self.__token_repository.get_all(user_id=command.user_id)

        for token in tokens:
            token.revoke()
            await self.__token_repository.update(token)

        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="REVOKE_ALL_USER_TOKENS_COMMAND",
            user_id=str(command.user_id),
            count=len(tokens),
        )
