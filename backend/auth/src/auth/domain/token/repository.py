from abc import ABC, abstractmethod
from typing import Any

from auth.domain.token.entity import RefreshToken


class TokenRepository(ABC):

    @abstractmethod
    async def add(self, entity: RefreshToken) -> None:
        """Create."""

    @abstractmethod
    async def update(self, entity: RefreshToken) -> None:
        """Update."""

    @abstractmethod
    async def get(self, **filters: Any) -> RefreshToken:
        """Get by id."""

    @abstractmethod
    async def delete(self, entity: RefreshToken) -> None:
        """Delete."""

    @abstractmethod
    async def get_all(self, **filters: Any) -> list[RefreshToken]:
        """Get all tokens matching filters."""

    @abstractmethod
    async def exists(self, **filters: Any) -> bool:
        """Check if exists."""
