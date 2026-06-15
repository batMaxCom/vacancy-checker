from typing import Any

from vacancy.application.operations.queries.source import (
    GetSourceByIdQuery,
    GetSourceByIdQueryHandler,
    GetSourceByPaginatedQuery,
    GetSourceByPaginatedQueryHandler,
    GetSourceBySelectListQuery,
    GetSourceBySelectListQueryHandler,
)
from vacancy.application.operations.queries.vacancy import (
    GetVacancyByIdQuery,
    GetVacancyByIdQueryHandler,
    GetVacancyByPaginatedQuery,
    GetVacancyByPaginatedQueryHandler,
)
from vacancy.application.ports.cqrs import BaseRequest, RequestHandler
from vacancy.infrastructure.mediator import Registry

QUERY_HANDLERS: list[tuple[type[BaseRequest[Any]], type[RequestHandler[Any, Any]]]] = [
    (GetSourceByIdQuery, GetSourceByIdQueryHandler),
    (GetSourceByPaginatedQuery, GetSourceByPaginatedQueryHandler),
    (GetSourceBySelectListQuery, GetSourceBySelectListQueryHandler),
    (GetVacancyByIdQuery, GetVacancyByIdQueryHandler),
    (GetVacancyByPaginatedQuery, GetVacancyByPaginatedQueryHandler),
]


def register_queries(registry: Registry) -> None:
    for query, handler in QUERY_HANDLERS:
        registry.add_request_handler(query, handler)
