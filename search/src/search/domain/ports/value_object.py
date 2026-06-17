from abc import ABC


class ValueObject(ABC):
    """Base class for value objects."""

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None: ...
