from dishka import AsyncContainer, make_async_container

from auth.entrypoint.di.providers.web import (
    ApplicationAdaptersProvider,
    DomainAdaptersProvider,
    FastapiProvider,
    HandlersProvider,
    LoggerAdapterProvider,
    MediatorProvider,
    WebConfigProvider,
    WebPersistenceProvider,
)
from auth.entrypoint.web.config import AppConfig, AuthConfig, PostgresConfig


def web_container(
        app_config: AppConfig,
        auth_settings: AuthConfig,
        db_config: PostgresConfig,
) -> AsyncContainer:
    return make_async_container(
        MediatorProvider(),
        WebConfigProvider(),
        WebPersistenceProvider(),
        DomainAdaptersProvider(),
        ApplicationAdaptersProvider(),
        FastapiProvider(),
        HandlersProvider(),
        LoggerAdapterProvider(),
        context={
            AppConfig: app_config,
            AuthConfig: auth_settings,
            PostgresConfig: db_config,
        }
    )
