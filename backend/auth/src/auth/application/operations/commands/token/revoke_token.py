from dataclasses import dataclass

from auth.application.ports import AsyncTransactionManager, Logger, TimeProvider
from auth.application.ports.cqrs import Command, CommandHandler
from auth.domain.token.repository import TokenRepository
from auth.domain.token.value_objects import TokenId


@dataclass(frozen=True, slots=True)
class RevokeRefreshTokenCommand(Command[None]):
    token_id: TokenId
    reason: str | None = None


class RevokeRefreshTokenCommandHandler(CommandHandler[RevokeRefreshTokenCommand, None]):
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

    async def handle(self, command: RevokeRefreshTokenCommand) -> None:
        token = await self.__token_repository.get(token_id=command.token_id)

        token.revoke()

        await self.__token_repository.update(token)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="REVOKE_REFRESH_TOKEN_COMMAND",
            token_id=str(command.token_id),
            reason=command.reason,
        )
