from abc import ABC, abstractmethod


class PasswordHasher(ABC):

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a password."""

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        """Verify a password against a hash."""

    @abstractmethod
    def extract_salt(self, password_hash: str) -> str:
        """Extract the salt from a password hash string."""
