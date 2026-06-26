from dishka import Provider, Scope, provide

from vacancy.application.ports.broker import EventConsumer, EventHandler
from vacancy.infrastructure.adapters.broker import KafkaEventConsumer, KafkaEventHandler


class KafkaBrokerProvider(Provider):
    scope = Scope.APP

    consumer = provide(KafkaEventConsumer, provides=EventConsumer)
    handler = provide(KafkaEventHandler, provides=EventHandler)
