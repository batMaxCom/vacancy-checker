from dishka import Provider, Scope, provide

from auth.domain.credential.repository import CredentialRepository
from auth.domain.token.repository import TokenRepository
from auth.infrastructure.persistence.adapters import CredentialRepositoryImpl, TokenRepositoryImpl

REPOSITORIES: list[tuple[type, type]] = [
    (CredentialRepositoryImpl, CredentialRepository),
    (TokenRepositoryImpl, TokenRepository),
]


class DomainAdaptersProvider(Provider):
    """Domain adapter provider."""

    scope = Scope.REQUEST

    for impl, interface in REPOSITORIES:
        locals()[f"{interface.__name__.lower()}"] = provide(
            impl, provides=interface, scope=Scope.REQUEST
        )
