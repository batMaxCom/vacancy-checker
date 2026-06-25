from dishka import AsyncContainer, make_async_container

from auth.entrypoint.di.providers.web import (
    ApplicationAdaptersProvider,
    BrokerProvider,
    DomainAdaptersProvider,
    FastapiProvider,
    HandlersProvider,
    LoggerAdapterProvider,
    MediatorProvider,
    WebConfigProvider,
    WebPersistenceProvider,
)
from auth.entrypoint.web.config import AppConfig, AuthConfig, PostgresConfig, RabbitMQConfig


def web_container(
        app_config: AppConfig,
        auth_settings: AuthConfig,
        db_config: PostgresConfig,
        broker_config: RabbitMQConfig,
) -> AsyncContainer:
    return make_async_container(
        MediatorProvider(),
        WebConfigProvider(),
        WebPersistenceProvider(),
        DomainAdaptersProvider(),
        ApplicationAdaptersProvider(),
        BrokerProvider(),
        FastapiProvider(),
        HandlersProvider(),
        LoggerAdapterProvider(),
        context={
            AppConfig: app_config,
            AuthConfig: auth_settings,
            PostgresConfig: db_config,
            RabbitMQConfig: broker_config,
        }
    )
