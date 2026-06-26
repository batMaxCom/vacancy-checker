from typing import Any

from auth.application.operations.queries.credential import (
    CheckEmailExistsQuery,
    CheckEmailExistsQueryHandler,
    GetUserCredentialByEmailQuery,
    GetUserCredentialByEmailQueryHandler,
    GetUserCredentialByUserIdQuery,
    GetUserCredentialByUserIdQueryHandler,
)
from auth.application.operations.queries.token import (
    GetActiveTokensByUserQuery,
    GetActiveTokensByUserQueryHandler,
    GetRefreshTokenByHashQuery,
    GetRefreshTokenByHashQueryHandler,
    ValidateRefreshTokenQuery,
    ValidateRefreshTokenQueryHandler,
)
from auth.application.ports.cqrs import BaseRequest, RequestHandler
from auth.infrastructure.mediator import Registry

QUERY_HANDLERS: list[tuple[type[BaseRequest[Any]], type[RequestHandler[Any, Any]]]] = [
    # Credential
    (GetUserCredentialByEmailQuery, GetUserCredentialByEmailQueryHandler),
    (GetUserCredentialByUserIdQuery, GetUserCredentialByUserIdQueryHandler),
    (CheckEmailExistsQuery, CheckEmailExistsQueryHandler),
    # Token
    (GetRefreshTokenByHashQuery, GetRefreshTokenByHashQueryHandler),
    (GetActiveTokensByUserQuery, GetActiveTokensByUserQueryHandler),
    (ValidateRefreshTokenQuery, ValidateRefreshTokenQueryHandler),
]


def register_queries(registry: Registry) -> None:
    for query, handler in QUERY_HANDLERS:
        registry.add_request_handler(query, handler)
