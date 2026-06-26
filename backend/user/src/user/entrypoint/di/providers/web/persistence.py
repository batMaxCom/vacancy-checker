from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from user.entrypoint.web.config import PostgresConfig


class WebPersistenceProvider(Provider):
    """Provider for PostgreSQL."""

    scope = Scope.APP

    @provide
    async def provide_postgres_engine(
        self, config: PostgresConfig
    ) -> AsyncIterable[AsyncEngine]:
        """Create an async PostgreSQL engine."""
        engine = create_async_engine(config.asyncpg_uri)
        yield engine
        await engine.dispose()

    @provide
    def provide_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        """Create an async PostgreSQL session maker."""
        return async_sessionmaker(bind=engine, expire_on_commit=False)

    @provide
    async def _provide_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        """Create an async database session."""
        async with session_maker() as session:
            yield session

    provide_session = provide(
        _provide_session,
        provides=AsyncSession,
        scope=Scope.REQUEST,
    )
