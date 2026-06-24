from dataclasses import dataclass


@dataclass(frozen=True)
class BaseRequest[TResponse]:
    """The general marker of the request."""


@dataclass(frozen=True)
class Command[TResponse](BaseRequest[TResponse]):
    """The command marker."""


@dataclass(frozen=True)
class Query[TResponse](BaseRequest[TResponse]):
    """The query marker."""
