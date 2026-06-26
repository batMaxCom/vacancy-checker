import asyncio
import json

from confluent_kafka import KafkaException, Message
from confluent_kafka.aio import AIOConsumer

from vacancy.application.ports.broker import EventConsumer, EventHandler
from vacancy.application.ports.logger import BrokerLogger
from vacancy.entrypoint.web.config import KafkaConfig

TOPICS = [
    "vacancy.created"
]

class KafkaEventConsumer(EventConsumer):

    def __init__(

        self,
        config: KafkaConfig,
        handler: EventHandler,
        logger: BrokerLogger,
    ) -> None:
        self._config = config
        self._handler = handler
        self._logger = logger

        self._topics: list[str] = TOPICS
        self._consumer: AIOConsumer | None = None

        self._task: asyncio.Task | None = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        if self._task:
            return

        self._stop_event.clear()

        self._task = asyncio.create_task(
            self._consume_loop(),
            name="kafka-consumer",
        )


    async def stop(self) -> None:
        self._stop_event.set()

        if self._task:
            await self._task

        if self._consumer:
            await self._consumer.close()

    async def _consume_loop(self) -> None:
        attempt = 0

        while not self._stop_event.is_set():

            try:
                await self._connect()

                attempt = 0

                consumer = self._consumer
                assert consumer is not None

                while not self._stop_event.is_set():

                    msg = await consumer.poll(
                        self._config.poll_timeout_seconds
                    )

                    if msg is None:
                        await asyncio.sleep(0)
                        continue

                    if msg.error():
                        raise KafkaException(msg.error())  # noqa: TRY301

                    await self._handle_message(msg)

            except Exception as exc:
                await self._logger.aexception(
                    "Kafka consumer failed: %s",
                    exc,
                )

                if attempt >= self._config.reconnect_attempts:
                    self._logger.error(  # noqa: TRY400
                        "Kafka reconnect limit reached",
                    )
                    return

                delay = min(
                    self._config.reconnect_initial_delay_seconds
                    * (2 ** attempt),
                    self._config.reconnect_max_delay_seconds,
                )

                attempt += 1

                self._logger.error(  # noqa: TRY400
                    "Reconnect in %s seconds",
                    delay,
                )

                await asyncio.sleep(delay)

    async def _connect(self) -> None:

        self._consumer = AIOConsumer(
            self._config.to_dict()
        )

        await self._consumer.subscribe(
            self._topics
        )

        self._logger.info(
            "Kafka consumer subscribed to %s",
            self._topics,
        )

    async def _handle_message(
        self,
        msg: Message,
    ) -> None:

        value = msg.value()
        if value is None:
            return

        payload = json.loads(value.decode())

        topic = msg.topic()
        if topic is None:
            return

        await self._logger.ainfo(
            event="KAFKA_CONSUMER_MESSAGE",
            topic=topic,
        )

        await self._handler.handle(
            event_type=topic,
            payload=payload,
        )
