from dataclasses import dataclass
from os import environ
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
