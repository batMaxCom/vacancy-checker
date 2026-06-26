import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import Connection, pool
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_engine_from_config

from vacancy.entrypoint.web.config.web import get_web_config
from vacancy.infrastructure.persistence.tables.base import MAPPER_REGISTRY

config = context.config
target_metadata = MAPPER_REGISTRY.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = get_web_config()

database_url = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.db_config.user,
    password=settings.db_config.password,
    host=settings.db_config.host,
    port=settings.db_config.port,
    database=settings.db_config.db,
)

config.set_main_option(
    "sqlalchemy.url", database_url.render_as_string(hide_password=False)
)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
