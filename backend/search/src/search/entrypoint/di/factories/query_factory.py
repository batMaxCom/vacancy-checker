from typing import Any

from search.application.operations.queries.search_job import (
    GetProfileJobsQuery,
    GetProfileJobsQueryHandler,
    GetSearchJobQuery,
    GetSearchJobQueryHandler,
)
from search.application.operations.queries.search_profile import (
    GetActiveProfilesQuery,
    GetActiveProfilesQueryHandler,
    GetSearchProfileQuery,
    GetSearchProfileQueryHandler,
    GetUserSearchProfilesQuery,
    GetUserSearchProfilesQueryHandler,
    GetUserSearchProfilesSelectQuery,
    GetUserSearchProfilesSelectQueryHandler,
)
from search.application.ports.cqrs import BaseRequest, RequestHandler
from search.infrastructure.mediator import Registry

QUERY_HANDLERS: list[tuple[type[BaseRequest[Any]], type[RequestHandler[Any, Any]]]] = [
    (GetSearchJobQuery, GetSearchJobQueryHandler),
    (GetProfileJobsQuery, GetProfileJobsQueryHandler),
    (GetSearchProfileQuery, GetSearchProfileQueryHandler),
    (GetUserSearchProfilesQuery, GetUserSearchProfilesQueryHandler),
    (GetActiveProfilesQuery, GetActiveProfilesQueryHandler),
    (GetUserSearchProfilesSelectQuery, GetUserSearchProfilesSelectQueryHandler),
]


def register_queries(registry: Registry) -> None:
    for query, handler in QUERY_HANDLERS:
        registry.add_request_handler(query, handler)
