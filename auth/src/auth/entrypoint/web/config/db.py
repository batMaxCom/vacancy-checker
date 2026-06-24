from dataclasses import dataclass
from os import environ
from typing import Self


@dataclass(frozen=True)
class PostgresConfig:
    """PostgreSQL configuration class."""

    host: str
    port: int
    user: str
    password: str
    db: str

    asyncpg_uri: str
    psycopg_uri: str

    @classmethod
    def from_env(cls) -> Self:
        """Return PostgreSQL settings from environment variables."""
        host = environ.get("POSTGRES_HOST", "localhost")
        port = int(environ.get("POSTGRES_PORT", "5432"))
        user = environ.get("POSTGRES_USER", "postgres")
        password = environ.get("POSTGRES_PASSWORD", "postgres")
        db = environ.get("POSTGRES_DATABASE", "postgres")

        asyncpg_uri = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
        psycopg_uri = f"postgresql://{user}:{password}@{host}:{port}/{db}"

        return cls(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            asyncpg_uri=asyncpg_uri,
            psycopg_uri=psycopg_uri,
        )
