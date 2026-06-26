from dishka import Provider, Scope, provide_all

from vacancy.application.operations.commands.source import (
    CreateSourceCommandHandler,
    UpdateSourceCommandHandler,
)
from vacancy.application.operations.commands.vacancy import (
    CreateVacancyCommandHandler,
    DeleteVacancyByProfileIdCommandHandler,
    UpdateVacancyCommandHandler,
)
from vacancy.application.operations.queries.source import (
    GetSourceByIdQueryHandler,
    GetSourceByPaginatedQueryHandler,
    GetSourceBySelectListQueryHandler,
)
from vacancy.application.operations.queries.vacancy import (
    GetVacancyByIdQueryHandler,
    GetVacancyByPaginatedQueryHandler,
)

COMMAND_HANDLERS: list[type] = [
    CreateSourceCommandHandler,
    UpdateSourceCommandHandler,
    CreateVacancyCommandHandler,
    DeleteVacancyByProfileIdCommandHandler,
    UpdateVacancyCommandHandler,
]

QUERY_HANDLERS: list[type] = [
    GetSourceByIdQueryHandler,
    GetSourceByPaginatedQueryHandler,
    GetSourceBySelectListQueryHandler,
    GetVacancyByIdQueryHandler,
    GetVacancyByPaginatedQueryHandler,
]


class HandlersProvider(Provider):
    """HTTP handlers"""

    # HTTP
    scope = Scope.REQUEST

    command_handlers = provide_all(*COMMAND_HANDLERS)
    query_handlers = provide_all(*QUERY_HANDLERS)
