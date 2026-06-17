from alembic.config import Config as AlembicConfig
from dishka import Provider, Scope, from_context
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from search.entrypoint.web.config.db import PostgresConfig


class CliWebConfigProvider(Provider):
    """Configuration provider for CLI commands."""

    scope = Scope.APP

    alembic_config = from_context(AlembicConfig)
    postgres_config = from_context(PostgresConfig)
    uvicorn_config = from_context(UvicornConfig)
    uvicorn_server = from_context(UvicornServer)
