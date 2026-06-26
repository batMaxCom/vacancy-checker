from click import Context, group, pass_context
from dishka.integrations.click import setup_dishka
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from vacancy.entrypoint.di.containers import cli_container
from vacancy.entrypoint.web.config import get_web_config
from vacancy.infrastructure.persistence.alembic.config import get_alembic_config
from vacancy.presentation.cli import (
    make_migrations,
    migrate,
    rollback,
    start_uvicorn,
)


@group()
@pass_context
def main(context: Context) -> None:
    """CLI for project API."""
    config  = get_web_config()
    app_config = config.app_config
    postgres_config = config.db_config
    alembic_config = get_alembic_config()
    uvicorn_config = UvicornConfig(
        app="vacancy.entrypoint.web.application:app_factory",
        host=app_config.server_host,
        port=app_config.server_port,
        loop=app_config.loop,
        factory=True,
        reload=True,
    )

    uvicorn_server = UvicornServer(uvicorn_config)

    container = cli_container(alembic_config, postgres_config, uvicorn_config, uvicorn_server)
    setup_dishka(container, context, finalize_container=True)

main.command(start_uvicorn)
main.command(make_migrations)
main.command(migrate)
main.command(rollback)
