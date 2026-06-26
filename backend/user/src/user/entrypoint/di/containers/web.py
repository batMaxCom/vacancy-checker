from dishka import AsyncContainer, make_async_container

from user.entrypoint.di.providers.web import (
    ApplicationAdaptersProvider,
    AuthAdaptersProvider,
    BrokerProvider,
    DomainAdaptersProvider,
    FastapiProvider,
    HandlersProvider,
    LoggerAdapterProvider,
    MediatorProvider,
    WebConfigProvider,
    WebPersistenceProvider,
)
from user.entrypoint.web.config import AppConfig, AuthConfig, PostgresConfig, RabbitMQConfig


def web_container(
        app_config: AppConfig,
        auth_config: AuthConfig,
        db_config: PostgresConfig,
        broker_config: RabbitMQConfig,
) -> AsyncContainer:
    context: dict = {
        AppConfig: app_config,
        AuthConfig: auth_config,
        PostgresConfig: db_config,
        RabbitMQConfig: broker_config,
    }

    return make_async_container(
        AuthAdaptersProvider(),
        BrokerProvider(),
        MediatorProvider(),
        WebConfigProvider(),
        WebPersistenceProvider(),
        DomainAdaptersProvider(),
        ApplicationAdaptersProvider(),
        FastapiProvider(),
        HandlersProvider(),
        LoggerAdapterProvider(),
        context=context,
    )
