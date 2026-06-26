from typing import Any

from user.application.operations.commands.user import (
    ActivateUserCommand,
    ActivateUserCommandHandler,
    ChangeRoleCommand,
    ChangeRoleCommandHandler,
    CreateUserCommand,
    CreateUserCommandHandler,
    DeleteUserByIdCommand,
    DeleteUserByIdCommandHandler,
    DeleteUserCommand,
    DeleteUserCommandHandler,
    SuspendUserCommand,
    SuspendUserCommandHandler,
    UpdateProfileCommand,
    UpdateProfileCommandHandler,
)
from user.application.ports.cqrs import BaseRequest, RequestHandler
from user.infrastructure.mediator.registry import Registry

COMMAND_HANDLERS: list[tuple[type[BaseRequest[Any]], type[RequestHandler[Any, Any]]]] = [
    (CreateUserCommand, CreateUserCommandHandler),
    (UpdateProfileCommand, UpdateProfileCommandHandler),
    (ChangeRoleCommand, ChangeRoleCommandHandler),
    (ActivateUserCommand, ActivateUserCommandHandler),
    (SuspendUserCommand, SuspendUserCommandHandler),
    (DeleteUserByIdCommand, DeleteUserByIdCommandHandler),
    (DeleteUserCommand, DeleteUserCommandHandler)
]

def register_commands(registry: Registry) -> None:
    for command, handler in COMMAND_HANDLERS:
        registry.add_request_handler(command, handler)
