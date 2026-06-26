from dishka import AsyncContainer, make_async_container

from vacancy.entrypoint.di.providers.web import (
    ApplicationAdaptersProvider,
    DomainAdaptersProvider,
    FastapiProvider,
    HandlersProvider,
    KafkaBrokerProvider,
    LoggerAdapterProvider,
    MediatorProvider,
    WebConfigProvider,
    WebPersistenceProvider, AuthAdaptersProvider,
)
from vacancy.entrypoint.web.config import AppConfig, KafkaConfig, PostgresConfig, AuthConfig


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
        FastapiProvider(),
        HandlersProvider(),
        LoggerAdapterProvider(),
        KafkaBrokerProvider(),
        context={
            AppConfig: app_config,
            AuthConfig: auth_config,
            PostgresConfig: db_config,
            KafkaConfig: broker_config
        }
    )
