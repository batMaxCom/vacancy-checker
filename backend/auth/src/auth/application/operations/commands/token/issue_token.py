from datetime import datetime
from dataclasses import dataclass

from auth.application.ports import AsyncTransactionManager, Logger, TimeProvider
from auth.application.ports.cqrs import Command, CommandHandler
from auth.domain.common.value_objects import UserId
from auth.domain.token.entity import RefreshToken
from auth.domain.token.repository import TokenRepository
from auth.domain.token.value_objects import TokenHash, TokenId


@dataclass(frozen=True, slots=True)
class IssueRefreshTokenCommand(Command[None]):
    token_id: TokenId
    user_id: UserId
    token_hash: TokenHash
    expires_at: datetime
    device_id: str | None = None
    ip_address: str = ""
    user_agent: str = ""


class IssueRefreshTokenCommandHandler(CommandHandler[IssueRefreshTokenCommand, None]):
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

    async def handle(self, command: IssueRefreshTokenCommand) -> None:
        token = RefreshToken(
            token_id=command.token_id,
            user_id=command.user_id,
            token_hash=command.token_hash,
            device_id=command.device_id,
            ip_address=command.ip_address,
            user_agent=command.user_agent,
            expires_at=command.expires_at,
        )

        await self.__token_repository.add(token)
        await self.__transaction_manager.commit()

        await self.__logger.ainfo(
            event="ISSUE_REFRESH_TOKEN_COMMAND",
            token_id=str(command.token_id),
            user_id=str(command.user_id),
        )
