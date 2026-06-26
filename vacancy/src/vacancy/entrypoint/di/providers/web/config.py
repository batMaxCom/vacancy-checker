from dishka import Provider, Scope, from_context

from vacancy.entrypoint.web.config import AppConfig, PostgresConfig, AuthConfig


class WebConfigProvider(Provider):
    """Application configuration provider."""

    scope = Scope.APP

    app_config = from_context(AppConfig)
    auth_config = from_context(AuthConfig)
    db_config = from_context(PostgresConfig)
