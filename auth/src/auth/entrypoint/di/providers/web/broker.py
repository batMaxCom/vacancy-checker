from collections.abc import AsyncIterator

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from dishka import Provider, Scope, provide

from auth.application.ports.broker.producer import EventProducer
from auth.entrypoint.web.config.broker import RabbitMQConfig
from auth.infrastructure.adapters.broker import RabbitMQEventProducer


class BrokerProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    async def get_connection(
        self,
        config: RabbitMQConfig,
    ) -> AsyncIterator[AbstractRobustConnection]:
        connection = await aio_pika.connect_robust(config.uri)
        try:
            yield connection
        finally:
            await connection.close()

    producer = provide(RabbitMQEventProducer, provides=EventProducer)

