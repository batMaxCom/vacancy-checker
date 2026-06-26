from dataclasses import dataclass, field
from enum import Enum, auto


class DomainTypeError(Enum):
    VALIDATION = auto()
    DOMAIN = auto()
    CONFLICT = auto()


@dataclass(frozen=True, slots=True)
class DomainError(Exception):
    type: DomainTypeError = field(default=DomainTypeError.DOMAIN)
    message: str = field(default="")
