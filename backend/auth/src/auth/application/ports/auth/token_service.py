from abc import ABC, abstractmethod


class TokenService(ABC):

    @abstractmethod
    def generate_access_token(self, payload: dict) -> str:
        """Generate a signed JWT access token."""

    @abstractmethod
    def verify_access_token(self, token: str) -> dict:
        """Verify and decode a JWT access token. Returns the payload."""
