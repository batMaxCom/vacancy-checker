from alembic.config import Config as AlembicConfig
from dishka import Container, make_container
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from search.entrypoint.di.providers.cli import (
    CliApplicationAdaptersProvider,
    CliWebConfigProvider,
    CliWebPersistenceProvider,
)
from search.entrypoint.web.config import PostgresConfig


def cli_container(
    alembic_config: AlembicConfig,
    db_config: PostgresConfig,
    uvicorn_config: UvicornConfig,
    uvicorn_server: UvicornServer
) -> Container:
    """Create a container for the CLI."""
    return make_container(
        CliWebConfigProvider(),
        CliWebPersistenceProvider(),
        CliApplicationAdaptersProvider(),
        context={
            AlembicConfig: alembic_config,
            UvicornConfig: uvicorn_config,
            UvicornServer: uvicorn_server,
            PostgresConfig: db_config,
        },
    )
