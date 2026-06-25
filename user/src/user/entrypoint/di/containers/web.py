from dishka import AsyncContainer, make_async_container

from user.entrypoint.di.providers.web import (
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
from user.entrypoint.web.config import AppConfig, PostgresConfig, RabbitMQConfig


def web_container(
        app_config: AppConfig,
        db_config: PostgresConfig,
        broker_config: RabbitMQConfig,
) -> AsyncContainer:
    context: dict = {
        AppConfig: app_config,
        PostgresConfig: db_config,
        RabbitMQConfig: broker_config,
    }

    return make_async_container(
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
