from dishka import Provider, Scope, alias, provide
from sqlalchemy.ext.asyncio import AsyncSession

from vacancy.application.ports import AsyncTransactionManager, TimeProvider, UUIDGenerator
from vacancy.application.ports.gateways import SourceGateway, VacancyGateway
from vacancy.domain.sources.repository import SourceRepository
from vacancy.domain.vacancies.repository import VacancyRepository
from vacancy.infrastructure.adapters import TimeProviderImpl, UUIDGeneratorImpl
from vacancy.infrastructure.persistence.adapters.gateways.source import SourceGatewayImpl
from vacancy.infrastructure.persistence.adapters.gateways.vacancy import VacancyGatewayImpl
from vacancy.infrastructure.persistence.adapters.repositories.source import SourceRepositoryImpl
from vacancy.infrastructure.persistence.adapters.repositories.vacancy import VacancyRepositoryImpl

GATEWAYS: list[tuple[type, type]] = [
    (SourceGatewayImpl, SourceGateway),
    (VacancyGatewayImpl, VacancyGateway),
]

REPOSITORIES: list[tuple[type, type]] = [
    (SourceRepositoryImpl, SourceRepository),
    (VacancyRepositoryImpl, VacancyRepository),
]


class ApplicationAdaptersProvider(Provider):
    """Application adapter provider."""

    scope = Scope.REQUEST

    for impl, interface in GATEWAYS:
        locals()[f"{interface.__name__.lower()}"] = provide(impl, provides=interface)

    for impl, interface in REPOSITORIES:
        locals()[f"{interface.__name__.lower()}"] = provide(impl, provides=interface)

    integer_id_generator = provide(UUIDGeneratorImpl, provides=UUIDGenerator)

    time_provider = provide(TimeProviderImpl, provides=TimeProvider)
    transaction_manager = alias(AsyncSession, provides=AsyncTransactionManager)
