from typing import cast

from vacancy.application.ports.cqrs import BaseRequest, RequestHandler, Resolver, Sender
from vacancy.infrastructure.common.infrastructure_errors import HandlerNotFoundError
from vacancy.infrastructure.mediator.registry import Registry


class BaseMediator[R: Resolver]:
    def __init__(self, resolver: R, registry: Registry) -> None:
        self._resolver = resolver
        self._registry = registry

    async def send[TResponse](self, request: BaseRequest[TResponse]) -> TResponse:
        request_type = type(request)
        handler_class = self._registry.get_request_handler(request_type)

        if not handler_class:
            raise HandlerNotFoundError(
                f"Handler for '{request_type.__name__}' not found."
            )
        handler = await self._resolver.resolve(handler_class)
        handler = cast(RequestHandler[BaseRequest[TResponse], TResponse], handler)
        return await handler.handle(request)


class MediatorImpl(BaseMediator[Resolver], Sender):
    def __init__(self, resolver: Resolver, registry: Registry) -> None:
        super().__init__(resolver, registry)
