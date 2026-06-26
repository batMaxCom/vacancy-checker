from dataclasses import dataclass

from auth.domain.common.domain_errors import DomainError, DomainTypeError
from auth.domain.ports import ValueObject


@dataclass(frozen=True, slots=True)
class Email(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if isinstance(self.value, str):
            object.__setattr__(self, "value", self.value.strip().lower())
        self._validate()

    def _validate(self) -> None:
        if not self.value:
            raise DomainError(type=DomainTypeError.VALIDATION, message="Email cannot be empty.")
        if "@" not in self.value:
            raise DomainError(type=DomainTypeError.VALIDATION, message="Invalid email format.")
