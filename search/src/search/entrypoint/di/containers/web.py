from dishka import AsyncContainer, make_async_container

from search.entrypoint.di.providers.web import (
    ApplicationAdaptersProvider,
    DomainAdaptersProvider,
    FastapiProvider,
    HandlersProvider,
    KafkaProvider,
    LoggerAdapterProvider,
    MediatorProvider,
    SearcherProvider,
    WebConfigProvider,
    WebPersistenceProvider,
)
from search.entrypoint.web.config import AppConfig, KafkaConfig, PostgresConfig


def web_container(
        app_config: AppConfig,
        db_config: PostgresConfig,
        broker_config: KafkaConfig,
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
        KafkaProvider(),
        context={
            AppConfig: app_config,
            PostgresConfig: db_config,
            KafkaConfig: broker_config
        }
    )
