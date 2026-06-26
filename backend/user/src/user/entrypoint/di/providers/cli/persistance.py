from collections.abc import Iterable

from dishka import Provider, Scope, provide
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from user.entrypoint.web.config.db import PostgresConfig


class CliWebPersistenceProvider(Provider):
    """Provider for PostgreSQL."""

    scope = Scope.APP

    @provide
    def provide_postgres_engine(self, config: PostgresConfig) -> Iterable[Engine]:
        """Create a PostgreSQL engine."""
        engine = create_engine(config.psycopg_uri)
        yield engine
        engine.dispose()

    @provide
    def provide_session_maker(self, engine: Engine) -> sessionmaker[Session]:
        """Create a PostgreSQL session maker."""
        return sessionmaker(bind=engine, expire_on_commit=False)

    @provide
    def provide_session(self, session_maker: sessionmaker[Session]) -> Iterable[Session]:
        """Create a database session."""
        with session_maker() as session:
            yield session
