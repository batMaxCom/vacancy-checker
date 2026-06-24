from abc import ABC, abstractmethod


class AuthServicePort(ABC):

    @abstractmethod
    async def login(self, email: str, password: str) -> dict:
        """Authenticate user and return tokens."""

    @abstractmethod
    async def refresh(self, refresh_token: str) -> dict:
        """Refresh access token using refresh token."""

    @abstractmethod
    async def logout(self, user_id: str, refresh_token: str) -> None:
        """Revoke refresh token."""
