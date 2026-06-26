from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from httpx import AsyncClient

from vacancy.application.ports.auth import AuthenticateProcessor, IdentityProvider, PermissionChecker
from vacancy.infrastructure.adapters.auth import (
    AuthenticateProcessorImpl,
    IdentityProviderImpl,
    PermissionCheckerImpl,
)


class AuthAdaptersProvider(Provider):
    scope = Scope.REQUEST

    authenticate_processor = provide(AuthenticateProcessorImpl, provides=AuthenticateProcessor)
    identity_provider = provide(IdentityProviderImpl, provides=IdentityProvider)
    permission_checker = provide(PermissionCheckerImpl, provides=PermissionChecker)

    @provide(scope=Scope.APP)
    async def get_http_client(self) -> AsyncIterator[AsyncClient]:
        async with AsyncClient() as client:
            yield client
