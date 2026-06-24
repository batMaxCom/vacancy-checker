from dataclasses import dataclass

from auth.domain.common.domain_errors import DomainError, DomainTypeError
from auth.domain.ports import ValueObject


@dataclass(frozen=True, slots=True)
class PasswordSalt(ValueObject):
    value: str | None = None

    def __post_init__(self) -> None:
        if self.value is not None and isinstance(self.value, str):
            object.__setattr__(self, "value", self.value.strip())
        self._validate()

    def _validate(self) -> None:
        if self.value is not None and not self.value:
            raise DomainError(type=DomainTypeError.VALIDATION, message="Password salt cannot be empty.")
