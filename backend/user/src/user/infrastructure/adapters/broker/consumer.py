import asyncio
import json

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractExchange,
    AbstractIncomingMessage,
    AbstractQueue,
    AbstractRobustConnection,
)

from user.application.ports.broker import EventConsumer, EventHandler
from user.application.ports.logger import Logger
from user.entrypoint.web.config.broker import RabbitMQConfig


class RabbitMQEventConsumer(EventConsumer):
    def __init__(
        self,
        config: RabbitMQConfig,
        handler: EventHandler,
        logger: Logger,
    ) -> None:
        self._config = config
        self._handler = handler
        self._logger = logger

        self._connection: AbstractRobustConnection | None = None
        self._task: asyncio.Task | None = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        if self._task:
            return

        self._stop_event.clear()

        self._task = asyncio.create_task(
            self._consume_loop(),
            name="rabbitmq-consumer",
        )

    async def stop(self) -> None:
        self._stop_event.set()

        if self._task:
            await self._task

        if self._connection:
            await self._connection.close()

    async def _consume_loop(self) -> None:
        attempt = 0

        while not self._stop_event.is_set():
            try:
                await self._connect()
                attempt = 0

                connection = self._connection
                assert connection is not None

                async with connection.channel() as channel:
                    exchange = await self._declare_exchange(channel)
                    queue = await self._declare_queue(channel)
                    await self._bind_queue(queue, exchange)

                    await self._logger.ainfo(
                        event="RABBITMQ_CONSUMER_STARTED",
                        queue=self._config.queue_name,
                        exchange=self._config.exchange_name,
                        routing_keys=self._config.routing_keys,
                    )

                    async with queue.iterator() as queue_iter:
                        async for message in queue_iter:
                            if self._stop_event.is_set():
                                break
                            await self._handle_message(message)

            except Exception as exc:
                await self._logger.aexception(
                    "RabbitMQ consumer failed: %s",
                    exc,
                )

                if attempt >= self._config.reconnect_attempts:
                    await self._logger.awarning(
                        event="RABBITMQ_RECONNECT_LIMIT_REACHED",
                        attempts=self._config.reconnect_attempts,
                    )
                    return

                delay = min(
                    self._config.reconnect_initial_delay_seconds * (2**attempt),
                    self._config.reconnect_max_delay_seconds,
                )

                attempt += 1

                await asyncio.sleep(delay)

    async def _connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self._config.uri)

    async def _declare_exchange(
        self,
        channel: AbstractChannel,
    ) -> AbstractExchange:
        return await channel.declare_exchange(
            name=self._config.exchange_name,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

    async def _declare_queue(
        self,
        channel: AbstractChannel,
    ) -> AbstractQueue:
        return await channel.declare_queue(
            name=self._config.queue_name,
            durable=True,
        )

    async def _bind_queue(
        self,
        queue: AbstractQueue,
        exchange: AbstractExchange,
    ) -> None:
        for routing_key in self._config.routing_keys:
            await queue.bind(exchange=exchange, routing_key=routing_key)

    async def _handle_message(
        self,
        message: AbstractIncomingMessage,
    ) -> None:
        async with message.process(requeue=True):
            body = message.body
            if not body:
                return

            payload = json.loads(body.decode())

            routing_key = message.routing_key or ""

            await self._logger.ainfo(
                event="RABBITMQ_CONSUMER_MESSAGE",
                routing_key=routing_key,
            )

            await self._handler.handle(
                event_type=routing_key,
                payload=payload,
            )
