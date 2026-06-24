from abc import ABC, abstractmethod

from auth.application.ports.auth.auth_context import AuthContext


class AuthenticationPort(ABC):

    @abstractmethod
    async def authenticate(self, access_token: str) -> AuthContext:
        """Validate an access token and return auth context."""
