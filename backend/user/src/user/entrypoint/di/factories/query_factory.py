from typing import Any

from user.application.operations.queries.user import (
    GetCurrentUserQuery,
    GetCurrentUserQueryHandler,
    GetUserByIdQuery,
    GetUserByIdQueryHandler,
    GetUsersQuery,
    GetUsersQueryHandler,
)
from user.application.ports.cqrs import BaseRequest, RequestHandler
from user.infrastructure.mediator import Registry

QUERY_HANDLERS: list[tuple[type[BaseRequest[Any]], type[RequestHandler[Any, Any]]]] = [
    (GetUserByIdQuery, GetUserByIdQueryHandler),
    (GetCurrentUserQuery, GetCurrentUserQueryHandler),
    (GetUsersQuery, GetUsersQueryHandler),
]


def register_queries(registry: Registry) -> None:
    for query, handler in QUERY_HANDLERS:
        registry.add_request_handler(query, handler)
