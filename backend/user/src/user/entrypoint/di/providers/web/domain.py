from dishka import Provider, Scope, provide

from user.domain.user.repository import UserRepository
from user.infrastructure.persistence.adapters.repositories import UserRepositoryImpl

REPOSITORIES: list[tuple[type, type]] = [
    (UserRepositoryImpl, UserRepository),
]

class DomainAdaptersProvider(Provider):
    """Domain adapter provider."""

    scope = Scope.REQUEST

    for impl, interface in REPOSITORIES:
        locals()[f"{interface.__name__.lower()}"] = provide(
            impl, provides=interface, scope=Scope.REQUEST
        )
