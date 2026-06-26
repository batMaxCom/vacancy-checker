from abc import ABC, abstractmethod
from datetime import datetime


class TimeProvider(ABC):
    @abstractmethod
    def current_time(self) -> datetime:
        """Return the current time in seconds."""

    @abstractmethod
    def current_timestamp(self) -> str:
        """Return the current time in milliseconds."""
