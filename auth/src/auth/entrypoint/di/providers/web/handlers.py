from dishka import Provider, Scope, provide_all

from auth.application.operations.commands.credential import (
    ChangePasswordCommandHandler,
    CreateUserCredentialCommandHandler,
    IncrementFailedLoginCommandHandler,
    LockAccountCommandHandler,
    ResetFailedLoginAttemptsCommandHandler,
    ResetPasswordCommandHandler,
    VerifyEmailCommandHandler,
)
from auth.application.operations.commands.token import (
    IssueRefreshTokenCommandHandler,
    RevokeAllUserTokensCommandHandler,
    RevokeRefreshTokenCommandHandler,
    RotateRefreshTokenCommandHandler,
)
from auth.application.operations.queries.credential import (
    CheckEmailExistsQueryHandler,
    GetUserCredentialByEmailQueryHandler,
    GetUserCredentialByUserIdQueryHandler,
)
from auth.application.operations.queries.token import (
    GetActiveTokensByUserQueryHandler,
    GetRefreshTokenByHashQueryHandler,
    ValidateRefreshTokenQueryHandler,
)

COMMAND_HANDLERS: list[type] = [
    # Credential
    CreateUserCredentialCommandHandler,
    VerifyEmailCommandHandler,
    ChangePasswordCommandHandler,
    ResetPasswordCommandHandler,
    LockAccountCommandHandler,
    IncrementFailedLoginCommandHandler,
    ResetFailedLoginAttemptsCommandHandler,
    # Token
    IssueRefreshTokenCommandHandler,
    RotateRefreshTokenCommandHandler,
    RevokeRefreshTokenCommandHandler,
    RevokeAllUserTokensCommandHandler,
]

QUERY_HANDLERS: list[type] = [
    # Credential
    GetUserCredentialByEmailQueryHandler,
    GetUserCredentialByUserIdQueryHandler,
    CheckEmailExistsQueryHandler,
    # Token
    GetRefreshTokenByHashQueryHandler,
    GetActiveTokensByUserQueryHandler,
    ValidateRefreshTokenQueryHandler,
]


class HandlersProvider(Provider):
    """HTTP handlers"""

    # HTTP
    scope = Scope.REQUEST

    command_handlers = provide_all(*COMMAND_HANDLERS)
    query_handlers = provide_all(*QUERY_HANDLERS)
