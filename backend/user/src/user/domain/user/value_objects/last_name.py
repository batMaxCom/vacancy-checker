from dataclasses import dataclass

from user.domain.common.domain_errors import DomainError, DomainTypeError
from user.domain.ports import ValueObject


@dataclass(frozen=True, slots=True)
class LastName(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if isinstance(self.value, str):
            object.__setattr__(self, "value", self.value.strip())
        self._validate()

    def _validate(self) -> None:
        if not self.value:
            raise DomainError(type=DomainTypeError.VALIDATION, message="Last name cannot be empty.")
