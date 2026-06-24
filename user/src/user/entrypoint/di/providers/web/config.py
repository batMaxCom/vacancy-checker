from dishka import Provider, Scope, from_context

from user.entrypoint.web.config import AppConfig, PostgresConfig


class WebConfigProvider(Provider):
    """Application configuration provider."""

    scope = Scope.APP

    app_config = from_context(AppConfig)
    db_config = from_context(PostgresConfig)
