from dishka import AsyncContainer, make_async_container

from user.entrypoint.di.providers.web import (
    ApplicationAdaptersProvider,
    DomainAdaptersProvider,
    FastapiProvider,
    HandlersProvider,
    LoggerAdapterProvider,
    MediatorProvider,
    WebConfigProvider,
    WebPersistenceProvider,
)
from user.entrypoint.web.config import AppConfig, PostgresConfig


def web_container(
        app_config: AppConfig,
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
            PostgresConfig: db_config,
        }
    )
