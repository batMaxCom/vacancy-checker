import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractRobustConnection

from auth.application.ports.broker.producer import EventProducer
from auth.application.ports.logger import Logger
from auth.entrypoint.web.config import RabbitMQConfig


class RabbitMQEventProducer(EventProducer):
    def __init__(
        self,
        connection: AbstractRobustConnection,
        broker_config: RabbitMQConfig,
        logger: Logger,
    ) -> None:
        self._connection = connection
        self._broker_config = broker_config
        self._logger = logger

    async def publish(self, routing_key: str, message: dict) -> None:
        await self._logger.ainfo(
            event="PUBLISH_EVENT",
            exchange=self._broker_config.exchange_name,
            routing_key=routing_key,
        )
        async with self._channel() as channel:
            exchange = await self._get_exchange(channel)
            body = json.dumps(message, default=str).encode()
            await exchange.publish(
                aio_pika.Message(body=body),
                routing_key=routing_key,
            )

    async def _get_exchange(self, channel: AbstractChannel) -> AbstractExchange:
        return await channel.declare_exchange(
            name=self._broker_config.exchange_name,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

    @asynccontextmanager
    async def _channel(self) -> AsyncIterator[AbstractChannel]:
        channel: AbstractChannel = await self._connection.channel()
        try:
            yield channel
        finally:
            await channel.close()
