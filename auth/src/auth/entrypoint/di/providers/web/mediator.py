from dishka import Provider, Scope, provide

from auth.application.ports.cqrs import Resolver, Sender
from auth.entrypoint.di.factories import register_commands, register_queries
from auth.infrastructure.mediator import DishkaResolver, MediatorImpl, Registry


class MediatorProvider(Provider):
    """Mediator provider."""

    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def provide_registry(self) -> Registry:
        registry = Registry()

        register_commands(registry)
        register_queries(registry)

        return registry

    mediator = provide(MediatorImpl, provides=Sender)
    resolver = provide(DishkaResolver, provides=Resolver)
