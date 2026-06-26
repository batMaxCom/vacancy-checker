from dataclasses import dataclass

from search.domain.common.domain_errors import DomainError, DomainTypeError


@dataclass(frozen=True, slots=True)
class Keyword:
    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", self.value.strip().lower())

        self._validate()

    def _validate(self) -> None:
        if not self.value:
            raise DomainError(
                type=DomainTypeError.VALIDATION,
                message="Keyword cannot be empty.",
            )
