from abc import ABC, abstractmethod
from typing import Any

from auth.domain.credential.entity import UserCredential


class CredentialRepository(ABC):

    @abstractmethod
    async def add(self, entity: UserCredential) -> None:
        """Create."""

    @abstractmethod
    async def update(self, entity: UserCredential) -> None:
        """Update."""

    @abstractmethod
    async def get(self, **filters: Any) -> UserCredential | None:
        """Get by id."""

    @abstractmethod
    async def delete(self, entity: UserCredential) -> None:
        """Delete."""

    @abstractmethod
    async def exists(self, **filters: Any) -> bool:
        """Check if exists."""
