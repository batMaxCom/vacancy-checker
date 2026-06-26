from dishka import AsyncContainer, make_async_container

from search.entrypoint.di.providers.web import (
    ApplicationAdaptersProvider,
    AuthAdaptersProvider,
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
from search.entrypoint.web.config import AppConfig, AuthConfig, KafkaConfig, PostgresConfig


def web_container(
        app_config: AppConfig,
        db_config: PostgresConfig,
        broker_config: KafkaConfig,
        auth_config: AuthConfig,
) -> AsyncContainer:
    return make_async_container(
        MediatorProvider(),
        WebConfigProvider(),
        WebPersistenceProvider(),
        DomainAdaptersProvider(),
        ApplicationAdaptersProvider(),
        AuthAdaptersProvider(),
        SearcherProvider(),
        FastapiProvider(),
        HandlersProvider(),
        LoggerAdapterProvider(),
        KafkaProvider(),
        context={
            AppConfig: app_config,
            AuthConfig: auth_config,
            PostgresConfig: db_config,
            KafkaConfig: broker_config,
        }
    )
