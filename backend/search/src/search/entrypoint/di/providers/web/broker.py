from collections.abc import AsyncIterator

from confluent_kafka.aio import AIOProducer
from dishka import Provider, Scope, provide

from search.application.ports.broker.publisher import EventPublisher
from search.entrypoint.web.config.broker import KafkaConfig
from search.infrastructure.adapters.broker.publisher import KafkaEventPublisher


class KafkaProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_producer(
        self,
        config: KafkaConfig,
    ) -> AsyncIterator[AIOProducer]:

        producer = AIOProducer(config.to_dict())

        try:
            yield producer
        finally:
            await producer.flush()
            await producer.close()

    @provide(scope=Scope.APP)
    def get_publisher(
        self,
        producer: AIOProducer,
    ) -> EventPublisher:
        return KafkaEventPublisher(producer)
