from dataclasses import dataclass

from search.domain.common.domain_errors import DomainError, DomainTypeError


@dataclass(frozen=True, slots=True)
class SearchInterval:
    minutes: int

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.minutes < 1:
            raise DomainError(
                type=DomainTypeError.VALIDATION,
                message="Search interval must be at least 1 minute.",
            )
