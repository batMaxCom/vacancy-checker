from alembic.command import downgrade as alembic_downgrade
from alembic.command import revision as alembic_revision
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from click import argument, option
from dishka import FromDishka
from dishka.integrations.click import inject


@option("--message", "-m", required=True, help="Migration message.")
@inject
def make_migrations(message: str, *, alembic_config: FromDishka[AlembicConfig]) -> None:
    """
    Create a new migration
    Usage: search-cli make-migrations -m 'message'.
    """
    alembic_revision(alembic_config, message=message, autogenerate=True)


@option("--revision", "-r", default="head", help="Run migration.")
@argument("revision", default="head")
@inject
def migrate(revision: str, *, alembic_config: FromDishka[AlembicConfig]) -> None:
    """
    Run migrations
    Usage: search-cli migrate -r 'message'.
    """
    alembic_upgrade(alembic_config, revision)


@option("--revision", "-r", default="-1", help="Rollback migration.")
@argument("revision", default="-1")
@inject
def rollback(revision: str, *, alembic_config: FromDishka[AlembicConfig]) -> None:
    """
    Rollback migration
    Usage: search-cli rollback.
    """
    alembic_downgrade(alembic_config, revision)
