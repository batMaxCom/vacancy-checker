from dishka import Provider, Scope, provide_all

from search.application.operations.commands.search_job import (
    RetrySearchJobCommandHandler,
    RunSearchCommandHandler,
)
from search.application.operations.commands.search_profile import (
    ActivateSearchProfileCommandHandler,
    AddKeywordCommandHandler,
    CreateSearchProfileCommandHandler,
    DeactivateSearchProfileCommandHandler,
    DeleteSearchProfileCommandHandler,
    RemoveKeywordCommandHandler,
    UpdateSearchProfileCommandHandler,
)
from search.application.operations.queries.search_job import (
    GetProfileJobsQueryHandler,
    GetSearchJobQueryHandler,
)
from search.application.operations.queries.search_profile import (
    GetActiveProfilesQueryHandler,
    GetSearchProfileQueryHandler,
    GetUserSearchProfilesQueryHandler,
)

COMMAND_HANDLERS: list[type] = [
    RunSearchCommandHandler,
    RetrySearchJobCommandHandler,
    ActivateSearchProfileCommandHandler,
    AddKeywordCommandHandler,
    CreateSearchProfileCommandHandler,
    DeactivateSearchProfileCommandHandler,
    DeleteSearchProfileCommandHandler,
    RemoveKeywordCommandHandler,
    UpdateSearchProfileCommandHandler,
]

QUERY_HANDLERS: list[type] = [
    GetSearchJobQueryHandler,
    GetProfileJobsQueryHandler,
    GetSearchProfileQueryHandler,
    GetUserSearchProfilesQueryHandler,
    GetActiveProfilesQueryHandler,
]


class HandlersProvider(Provider):
    """HTTP handlers"""

    # HTTP
    scope = Scope.REQUEST

    command_handlers = provide_all(*COMMAND_HANDLERS)
    query_handlers = provide_all(*QUERY_HANDLERS)
