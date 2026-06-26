from dishka import Provider, Scope, provide_all

from user.application.operations.commands.user import (
    ActivateUserCommandHandler,
    ChangeRoleCommandHandler,
    CreateUserCommandHandler,
    DeleteUserByIdCommandHandler,
    DeleteUserCommandHandler,
    SuspendUserCommandHandler,
    UpdateProfileCommandHandler,
)
from user.application.operations.queries.user import (
    GetCurrentUserQueryHandler,
    GetUserByIdQueryHandler,
    GetUsersQueryHandler,
)

COMMAND_HANDLERS: list[type] = [
    CreateUserCommandHandler,
    UpdateProfileCommandHandler,
    ChangeRoleCommandHandler,
    ActivateUserCommandHandler,
    SuspendUserCommandHandler,
    DeleteUserByIdCommandHandler,
    DeleteUserCommandHandler
]

QUERY_HANDLERS: list[type] = [
    GetUserByIdQueryHandler,
    GetCurrentUserQueryHandler,
    GetUsersQueryHandler,
]


class HandlersProvider(Provider):
    """HTTP handlers"""

    # HTTP
    scope = Scope.REQUEST

    command_handlers = provide_all(*COMMAND_HANDLERS)
    query_handlers = provide_all(*QUERY_HANDLERS)
