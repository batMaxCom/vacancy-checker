from dataclasses import dataclass, field


@dataclass(frozen=True)
class Response:
    """Response class for query results."""

    status_code: int

@dataclass(frozen=True)
class SuccessfulResponse[TResult](Response):
    """Класс реализующий успешный ответ на запрос."""

    result: TResult | None = field(default=None)

@dataclass(frozen=True)
class ErrorResponse(Response):
    error: str
