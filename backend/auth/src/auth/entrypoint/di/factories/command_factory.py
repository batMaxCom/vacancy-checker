from typing import Any

from auth.application.operations.commands.credential import (
    ChangePasswordCommand,
    ChangePasswordCommandHandler,
    CreateUserCredentialCommand,
    CreateUserCredentialCommandHandler,
    IncrementFailedLoginCommand,
    IncrementFailedLoginCommandHandler,
    LockAccountCommand,
    LockAccountCommandHandler,
    ResetFailedLoginAttemptsCommand,
    ResetFailedLoginAttemptsCommandHandler,
    ResetPasswordCommand,
    ResetPasswordCommandHandler,
    VerifyEmailCommand,
    VerifyEmailCommandHandler,
)
from auth.application.operations.commands.token import (
    IssueRefreshTokenCommand,
    IssueRefreshTokenCommandHandler,
    RevokeAllUserTokensCommand,
    RevokeAllUserTokensCommandHandler,
    RevokeRefreshTokenCommand,
    RevokeRefreshTokenCommandHandler,
    RotateRefreshTokenCommand,
    RotateRefreshTokenCommandHandler,
)
from auth.application.ports.cqrs import BaseRequest, RequestHandler
from auth.infrastructure.mediator.registry import Registry

COMMAND_HANDLERS: list[tuple[type[BaseRequest[Any]], type[RequestHandler[Any, Any]]]] = [
    # Credential
    (CreateUserCredentialCommand, CreateUserCredentialCommandHandler),
    (VerifyEmailCommand, VerifyEmailCommandHandler),
    (ChangePasswordCommand, ChangePasswordCommandHandler),
    (ResetPasswordCommand, ResetPasswordCommandHandler),
    (LockAccountCommand, LockAccountCommandHandler),
    (IncrementFailedLoginCommand, IncrementFailedLoginCommandHandler),
    (ResetFailedLoginAttemptsCommand, ResetFailedLoginAttemptsCommandHandler),
    # Token
    (IssueRefreshTokenCommand, IssueRefreshTokenCommandHandler),
    (RotateRefreshTokenCommand, RotateRefreshTokenCommandHandler),
    (RevokeRefreshTokenCommand, RevokeRefreshTokenCommandHandler),
    (RevokeAllUserTokensCommand, RevokeAllUserTokensCommandHandler),
]


def register_commands(registry: Registry) -> None:
    for command, handler in COMMAND_HANDLERS:
        registry.add_request_handler(command, handler)
