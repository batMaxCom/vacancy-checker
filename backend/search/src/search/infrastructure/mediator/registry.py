from search.application.ports.cqrs import BaseRequest, RequestHandler


class Registry:
    """Registering handlers."""

    __request_handlers: dict[type[BaseRequest], type[RequestHandler]]

    def __init__(self) -> None:
        self.__request_handlers = {}

    def add_request_handler(
        self,
        request_type: type[BaseRequest],
        request_handler: type[RequestHandler],
    ) -> None:
        """Add a request handler."""
        self.__request_handlers[request_type] = request_handler

    def get_request_handler(
        self, request_type: type[BaseRequest]
    ) -> type[RequestHandler] | None:
        """Get request handler."""
        return self.__request_handlers.get(request_type)
