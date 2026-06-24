from dishka import Provider, Scope, alias, provide
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.ports import (
    AsyncTransactionManager,
    PasswordHasher,
    TimeProvider,
    UUIDGenerator,
)
from auth.application.ports.auth import AuthServicePort, AuthenticationPort, TokenService
from auth.infrastructure.adapters import (
    AuthServicePortImpl,
    AuthenticationPortImpl,
    PasswordHasherImpl,
    TimeProviderImpl,
    TokenServiceImpl,
    UUIDGeneratorImpl,
)

GATEWAYS: list[tuple[type, type]] = [
    # Example
    #(GatewayImpl, Gateway),
]


class ApplicationAdaptersProvider(Provider):
    """Application adapter provider."""

    scope = Scope.REQUEST

    for impl, interface in GATEWAYS:
        locals()[f"{interface.__name__.lower()}"] = provide(impl, provides=interface)

    integer_id_generator = provide(UUIDGeneratorImpl, provides=UUIDGenerator)

    time_provider = provide(TimeProviderImpl, provides=TimeProvider)
    transaction_manager = alias(AsyncSession, provides=AsyncTransactionManager)

    password_hasher = provide(PasswordHasherImpl, provides=PasswordHasher)
    token_service = provide(TokenServiceImpl, provides=TokenService)
    auth_service = provide(AuthServicePortImpl, provides=AuthServicePort)
    authentication = provide(AuthenticationPortImpl, provides=AuthenticationPort)

