from abc import ABC, abstractmethod


class AsyncTransactionManager(ABC):
    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""

    @abstractmethod
    async def flush(self) -> None:
        """Flushes the current transaction."""

    @abstractmethod
    async def rollback(self) -> None:
        """Roll back the current transaction."""


class SyncTransactionManager(ABC):
    @abstractmethod
    def commit(self) -> None:
        """Commit the current transaction."""

    @abstractmethod
    def flush(self) -> None:
        """Flushes the current transaction."""

    @abstractmethod
    def rollback(self) -> None:
        """Roll back the current transaction."""
