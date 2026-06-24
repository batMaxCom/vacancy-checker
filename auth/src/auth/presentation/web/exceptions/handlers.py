from dataclasses import asdict
from typing import Final

from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from auth.application.common.application_error import (
    ApplicationError,
    ApplicationTypeError,
)
from auth.domain.common.domain_errors import DomainError, DomainTypeError
from auth.infrastructure.common.infrastructure_errors import InfrastructureError
from auth.presentation.web.schemas.base import ErrorResponse

STATUS_MAP: Final[dict[ApplicationTypeError | DomainTypeError, int]] = {
    ApplicationTypeError.UNAUTHORIZED: HTTP_401_UNAUTHORIZED,
    ApplicationTypeError.FORBIDDEN: HTTP_403_FORBIDDEN,
    ApplicationTypeError.NOT_FOUND: HTTP_404_NOT_FOUND,
    ApplicationTypeError.CONFLICT: HTTP_409_CONFLICT,
    DomainTypeError.VALIDATION: HTTP_422_UNPROCESSABLE_CONTENT,
    DomainTypeError.CONFLICT: HTTP_409_CONFLICT,
}


def application_error_handler(_: Request, exception: ApplicationError) -> Response:
    """Application error handler."""
    status_code = STATUS_MAP[exception.type]
    error_response = ErrorResponse(status_code, exception.message)
    return JSONResponse(status_code=status_code, content=asdict(error_response))


def domain_error_handler(_: Request, exception: DomainError) -> Response:
    """Domain error handler."""
    status_code = STATUS_MAP[exception.type]
    error_response = ErrorResponse(status_code, exception.message)
    return JSONResponse(status_code=status_code, content=asdict(error_response))


def internal_error_handler(
    _: Request, exception: InfrastructureError | Exception
) -> Response:
    """Infrastructure error handler."""
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    message = exception.message if hasattr(exception, "message") else str(exception)
    error_response = ErrorResponse(status_code, message)
    return JSONResponse(status_code=status_code, content=asdict(error_response))
