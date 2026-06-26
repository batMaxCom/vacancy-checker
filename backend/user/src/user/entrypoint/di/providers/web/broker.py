from dishka import Provider, Scope, provide

from user.application.ports.broker import EventConsumer, EventHandler
from user.infrastructure.adapters.broker import RabbitMQEventConsumer, RabbitMQEventHandler


class BrokerProvider(Provider):
    scope = Scope.APP

    consumer = provide(RabbitMQEventConsumer, provides=EventConsumer)
    handler = provide(RabbitMQEventHandler, provides=EventHandler)
