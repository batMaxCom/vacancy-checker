from dataclasses import dataclass, field
from enum import Enum, auto


class InfraErrorType(Enum):
    INFRASTRUCTURE = auto()


@dataclass(slots=True)
class InfrastructureError(Exception):
    message: str = field(default="Error in implementation.")
    type: InfraErrorType = field(default=InfraErrorType.INFRASTRUCTURE)
    """General class for infrastructure errors."""


@dataclass(slots=True)
class HandlerNotFoundError(InfrastructureError):
    """Error if CQRS handler is not found."""
