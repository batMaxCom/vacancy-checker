from dataclasses import dataclass
from os import environ
from typing import Self


@dataclass(slots=True, frozen=True)
class AuthConfig:
    authenticate_url: str

    @classmethod
    def from_env(cls) -> Self:
        """Возвращает настройки приложения."""
        authenticate_url = environ.get(
            "AUTHENTICATE_URL",
            default="http://localhost:9000/api/v1/auth/authenticate",
        )
        return cls(authenticate_url=authenticate_url)
