from dishka import Provider, Scope, alias, provide
from sqlalchemy.ext.asyncio import AsyncSession

from search.application.ports import AsyncTransactionManager, TimeProvider, UUIDGenerator
from search.application.ports.gateways import SearchJobGateway, SearchProfileGateway
from search.infrastructure.adapters import TimeProviderImpl, UUIDGeneratorImpl
from search.infrastructure.persistence.adapters.gateways import (
    SearchJobGatewayImpl,
    SearchProfileGatewayImpl,
)

GATEWAYS: list[tuple[type, type]] = [
    (SearchJobGatewayImpl, SearchJobGateway),
    (SearchProfileGatewayImpl, SearchProfileGateway),
]


class ApplicationAdaptersProvider(Provider):
    """Application adapter provider."""

    scope = Scope.REQUEST

    for impl, interface in GATEWAYS:
        locals()[f"{interface.__name__.lower()}"] = provide(impl, provides=interface)

    integer_id_generator = provide(UUIDGeneratorImpl, provides=UUIDGenerator)

    time_provider = provide(TimeProviderImpl, provides=TimeProvider)
    transaction_manager = alias(AsyncSession, provides=AsyncTransactionManager)
