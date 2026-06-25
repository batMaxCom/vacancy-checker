from dataclasses import dataclass, field
from os import getenv, environ
from typing import Self


@dataclass(frozen=True)
class AppConfig:
    """Application configuration."""

    server_host: str
    server_port: int
    open_api_schema_path: str
    docs_path: str
    cors_origins: list[str]
    loop: str
    debug: bool

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            server_host=environ.get("SERVER_HOST", "127.0.0.1"),
            server_port=int(environ.get("SERVER_PORT", "8000")),
            open_api_schema_path=environ.get("OPEN_API_SCHEMA_PATH", "/openapi.json"),
            docs_path=environ.get("DOCS_PATH", "/docs"),
            cors_origins=environ.get("CORS_ORIGINS", "*").split(","),
            loop=environ.get("LOOP", "auto"),
            debug=bool(environ.get("DEBUG", "False")),
        )


@dataclass(frozen=True)
class GatewayConfig:
    """Gateway configuration."""

    auth_url: str
    user_url: str
    search_url: str
    vacancy_url: str

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            auth_url=getenv("AUTH_URL", "http://127.0.0.1:8003"),
            user_url=getenv("USER_URL", "http://127.0.0.1:8002"),
            search_url=getenv("SEARCH_URL", "http://127.0.0.1:8000"),
            vacancy_url=getenv("VACANCY_URL", "http://127.0.0.1:8001"),
        )
