from abc import ABC, abstractmethod

from auth.application.ports.auth.auth_context import AuthContext


class AuthenticationPort(ABC):

    @abstractmethod
    async def authenticate(self) -> AuthContext:
        """Validate an access token and return auth context."""
