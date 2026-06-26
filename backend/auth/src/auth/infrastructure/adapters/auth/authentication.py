import jwt

from fastapi import Request

from auth.application.common.application_error import ApplicationError, ApplicationTypeError
from auth.application.common.const.errors import INVALID_TOKEN, UNAUTHENTICATED
from auth.application.ports.auth import AuthenticationPort, AuthContext, TokenService
from auth.entrypoint.web.config import AuthConfig


class AuthenticationPortImpl(AuthenticationPort):
    def __init__(
        self,
        token_service: TokenService,
        settings: AuthConfig,
        request: Request
    ) -> None:
        self.__token_service = token_service
        self.__settings = settings
        self.__request = request

    async def authenticate(self) -> AuthContext:
        try:
            access_token = self.__request.headers.get("x-access-token")
            if access_token is None:
                raise ApplicationError(
                    type=ApplicationTypeError.UNAUTHORIZED,
                    message=UNAUTHENTICATED,
                )
            payload = self.__token_service.verify_access_token(access_token)
        except jwt.ExpiredSignatureError:
            raise ApplicationError(
                type=ApplicationTypeError.UNAUTHORIZED,
                message=INVALID_TOKEN,
            )
        except jwt.PyJWTError:
            raise ApplicationError(
                type=ApplicationTypeError.UNAUTHORIZED,
                message=INVALID_TOKEN,
            )

        return AuthContext(
            user_id=payload.get("sub", ""),
            role=payload.get("role", ""),
            is_valid=True,
            expires_at=payload.get("exp"),
        )
