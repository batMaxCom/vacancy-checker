from datetime import UTC, datetime, timedelta

import jwt

from auth.application.ports.auth import TokenService
from auth.entrypoint.web.config import AuthConfig


class TokenServiceImpl(TokenService):
    def __init__(self, settings: AuthConfig) -> None:
        self.__settings = settings

    def generate_access_token(self, payload: dict) -> str:
        now = datetime.now(UTC)
        payload = {
            **payload,
            "iat": now,
            "exp": now + timedelta(seconds=self.__settings.access_token_expires_seconds),
        }
        return jwt.encode(payload, self.__settings.secret_key, algorithm="HS256")

    def verify_access_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.__settings.secret_key,
            algorithms=["HS256"],
        )
