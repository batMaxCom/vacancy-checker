from abc import ABC, abstractmethod
from typing import Any

from user.domain.user.entity import User


class UserRepository(ABC):

    @abstractmethod
    async def add(self, entity: User) -> None:
        """Create."""

    @abstractmethod
    async def update(self, entity: User) -> None:
        """Update."""

    @abstractmethod
    async def get(self, **filters: Any) -> User:
        """Get by id."""

    @abstractmethod
    async def delete(self, entity: User) -> None:
        """Delete."""

    @abstractmethod
    async def exists(self, **filters: Any) -> bool:
        """Check if exists."""

    @abstractmethod
    async def get_all(self, **filters: Any) -> list[User]:
        """Get all users matching filters."""
