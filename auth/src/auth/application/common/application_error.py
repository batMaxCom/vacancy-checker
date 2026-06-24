from dataclasses import dataclass, field
from enum import Enum, auto


class ApplicationTypeError(Enum):
    NOT_FOUND = auto()
    APPLICATION = auto()
    UNAUTHORIZED = auto()
    FORBIDDEN = auto()
    CONFLICT = auto()


@dataclass(frozen=True, slots=True)
class ApplicationError(Exception):
    type: ApplicationTypeError = field(default=ApplicationTypeError.APPLICATION)
    message: str = field(default="")
