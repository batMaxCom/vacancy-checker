from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from auth.application.operations.commands.credential import (
    IncrementFailedLoginCommand,
    ResetFailedLoginAttemptsCommand,
)
from auth.application.operations.commands.token import (
    IssueRefreshTokenCommand,
    RevokeRefreshTokenCommand,
    RotateRefreshTokenCommand,
)
from auth.application.operations.queries.credential import (
    GetUserCredentialByEmailQuery,
)
from auth.application.operations.queries.token import (
    GetRefreshTokenByHashQuery,
    ValidateRefreshTokenQuery,
)
from auth.application.ports import Logger, PasswordHasher
from auth.application.ports.auth import AuthServicePort, TokenService
from auth.application.ports.cqrs import Sender
from auth.domain.common.value_objects import UserId
from auth.domain.credential.value_objects import Email
from auth.domain.token.value_objects import TokenHash, TokenId
from auth.entrypoint.web.config import AuthConfig
from auth.infrastructure.adapters.auth.utils import generate_token_hash


class AuthServicePortImpl(AuthServicePort):
    def __init__(
        self,
        sender: Sender,
        password_hasher: PasswordHasher,
        token_service: TokenService,
        settings: AuthConfig,
        logger: Logger,
    ) -> None:
        self.__sender = sender
        self.__password_hasher = password_hasher
        self.__token_service = token_service
        self.__settings = settings
        self.__logger = logger

    async def login(self, email: str, password: str) -> dict:
        credential_dto = await self.__sender.send(
            GetUserCredentialByEmailQuery(email=Email(email)),
        )

        if credential_dto is None:
            raise ValueError("Invalid credentials")

        user_id = UserId(UUID(credential_dto.user_id))

        if not self.__password_hasher.verify(password, credential_dto.password_hash):
            await self.__sender.send(
                IncrementFailedLoginCommand(user_id=user_id),
            )
            raise ValueError("Invalid credentials")

        await self.__sender.send(
            ResetFailedLoginAttemptsCommand(user_id=user_id),
        )

        access_token = self.__token_service.generate_access_token(
            {"sub": credential_dto.user_id, "role": "user"},
        )

        raw_refresh, refresh_hash = generate_token_hash()

        await self.__sender.send(
            IssueRefreshTokenCommand(
                token_id=TokenId(uuid4()),
                user_id=user_id,
                token_hash=TokenHash(value=refresh_hash),
                expires_at=datetime.now(UTC)
                + timedelta(seconds=self.__settings.refresh_token_expires_seconds),
            ),
        )

        await self.__logger.ainfo(event="LOGIN_SUCCESS", user_id=str(user_id))

        return {
            "access_token": access_token,
            "refresh_token": raw_refresh,
            "token_type": "bearer",
        }

    async def refresh(self, refresh_token: str) -> dict:
        from auth.infrastructure.adapters.auth.utils import hash_token

        token_hash_str = hash_token(refresh_token)
        old_token_dto = await self.__sender.send(
            GetRefreshTokenByHashQuery(token_hash=TokenHash(value=token_hash_str)),
        )

        if old_token_dto is None:
            raise ValueError("Invalid refresh token")

        old_token_id = TokenId(UUID(old_token_dto.token_id))
        user_id = UserId(UUID(old_token_dto.user_id))

        is_valid = await self.__sender.send(
            ValidateRefreshTokenQuery(token_hash=TokenHash(value=token_hash_str)),
        )
        if not is_valid:
            raise ValueError("Refresh token expired or revoked")

        raw_new_token, new_token_hash_str = generate_token_hash()

        await self.__sender.send(
            RotateRefreshTokenCommand(
                old_token_id=old_token_id,
                new_token_id=TokenId(uuid4()),
                user_id=user_id,
                token_hash=TokenHash(value=new_token_hash_str),
                expires_at=datetime.now(UTC)
                + timedelta(seconds=self.__settings.refresh_token_expires_seconds),
            ),
        )

        access_token = self.__token_service.generate_access_token(
            {"sub": str(user_id), "role": "user"},
        )

        await self.__logger.ainfo(event="REFRESH_SUCCESS", user_id=str(user_id))

        return {
            "access_token": access_token,
            "refresh_token": raw_new_token,
            "token_type": "bearer",
        }

    async def logout(self, user_id: str, refresh_token: str) -> None:
        from auth.infrastructure.adapters.auth.utils import hash_token

        token_hash_str = hash_token(refresh_token)
        token_dto = await self.__sender.send(
            GetRefreshTokenByHashQuery(token_hash=TokenHash(value=token_hash_str)),
        )

        if token_dto is None:
            return

        await self.__sender.send(
            RevokeRefreshTokenCommand(
                    token_id=TokenId(UUID(token_dto.token_id)),
                reason="logout",
            ),
        )

        await self.__logger.ainfo(event="LOGOUT_SUCCESS", user_id=user_id)
