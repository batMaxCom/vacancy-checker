import json

from confluent_kafka.aio import AIOProducer

from search.application.ports.broker.publisher import EventPublisher


class KafkaEventPublisher(EventPublisher):

    def __init__(self, producer: AIOProducer) -> None:
        self._producer = producer

    async def publish(self, topic: str, payload: dict) -> None:
        data = json.dumps(payload).encode()
        delivery_report = await self._producer.produce(
            topic=topic,
            value=data,
        )
        await delivery_report
