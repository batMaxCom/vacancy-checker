from dishka import AsyncContainer, make_async_container

from search.entrypoint.di.providers.web import (
    ApplicationAdaptersProvider,
    DomainAdaptersProvider,
    FastapiProvider,
    HandlersProvider,
    LoggerAdapterProvider,
    MediatorProvider,
    SearcherProvider,
    WebConfigProvider,
    WebPersistenceProvider,
)
from search.entrypoint.web.config import AppConfig, PostgresConfig


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
        SearcherProvider(),
        FastapiProvider(),
        HandlersProvider(),
        LoggerAdapterProvider(),
        context={
            AppConfig: app_config,
            PostgresConfig: db_config,
        }
    )
