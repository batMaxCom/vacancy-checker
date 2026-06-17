from dishka import Provider, Scope, provide

from search.domain.search_job.repository import SearchJobRepository
from search.domain.search_profile.repository import SearchProfileRepository
from search.infrastructure.persistence.adapters.repositories import (
    SearchJobRepositoryImpl,
    SearchProfileRepositoryImpl,
)

REPOSITORIES: list[tuple[type, type]] = [
    (SearchJobRepositoryImpl, SearchJobRepository),
    (SearchProfileRepositoryImpl, SearchProfileRepository),
]

class DomainAdaptersProvider(Provider):
    """Domain adapter provider."""

    scope = Scope.REQUEST

    for impl, interface in REPOSITORIES:
        locals()[f"{interface.__name__.lower()}"] = provide(
            impl, provides=interface, scope=Scope.REQUEST
        )
