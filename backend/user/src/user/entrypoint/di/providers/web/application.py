from dishka import Provider, Scope, alias, provide
from sqlalchemy.ext.asyncio import AsyncSession

from user.application.ports import AsyncTransactionManager, TimeProvider, UUIDGenerator
from user.application.ports.gateways.user import UserGateway
from user.infrastructure.adapters import TimeProviderImpl, UUIDGeneratorImpl
from user.infrastructure.persistence.adapters.gateways import UserGatewayImpl

GATEWAYS: list[tuple[type, type]] = [
    (UserGatewayImpl, UserGateway),
]


class ApplicationAdaptersProvider(Provider):
    """Application adapter provider."""

    scope = Scope.REQUEST

    for impl, interface in GATEWAYS:
        locals()[f"{interface.__name__.lower()}"] = provide(impl, provides=interface)

    integer_id_generator = provide(UUIDGeneratorImpl, provides=UUIDGenerator)

    time_provider = provide(TimeProviderImpl, provides=TimeProvider)
    transaction_manager = alias(AsyncSession, provides=AsyncTransactionManager)
