from dataclasses import dataclass
from os import environ
from typing import Self


@dataclass(frozen=True, slots=True)
class AuthConfig:
    secret_key: str
    access_token_expires_seconds: int
    refresh_token_expires_seconds: int

    @classmethod
    def from_env(cls) -> Self:
        """Возвращает настройки RabbitMQ."""
        secret_key = environ.get("SECRET_KEY", "changeme")
        access_token_expires_seconds = int(environ.get("ACCESS_TOKEN_EXPIRES_SECONDS", "900"))
        refresh_token_expires_seconds = int(environ.get("REFRESH_TOKEN_EXPIRES_SECONDS", "2_592_000"))

        return cls(
            secret_key=secret_key,
            access_token_expires_seconds=access_token_expires_seconds,
            refresh_token_expires_seconds=refresh_token_expires_seconds,
        )
