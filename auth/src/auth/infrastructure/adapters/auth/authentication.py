import jwt

from auth.application.ports.auth import AuthenticationPort, AuthContext, TokenService
from auth.entrypoint.web.config import AuthConfig


class AuthenticationPortImpl(AuthenticationPort):
    def __init__(
        self,
        token_service: TokenService,
        settings: AuthConfig,
    ) -> None:
        self.__token_service = token_service
        self.__settings = settings

    async def authenticate(self, access_token: str) -> AuthContext:
        try:
            payload = self.__token_service.verify_access_token(access_token)
        except jwt.ExpiredSignatureError:
            return AuthContext(user_id="", role="", is_valid=False)
        except jwt.PyJWTError:
            return AuthContext(user_id="", role="", is_valid=False)

        return AuthContext(
            user_id=payload.get("sub", ""),
            role=payload.get("role", ""),
            is_valid=True,
            expires_at=payload.get("exp"),
        )
