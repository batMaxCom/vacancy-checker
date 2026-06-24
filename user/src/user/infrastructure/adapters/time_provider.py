from datetime import UTC, datetime

from user.application.ports.time_provider import TimeProvider


class TimeProviderImpl(TimeProvider):
    """Class that implements work with time."""

    def current_time(self) -> datetime:
        return datetime.now(UTC)

    def current_timestamp(self) -> str:
        return datetime.now(UTC).strftime("%y-%m-%dT%H-%M-%S")
