from typing import TYPE_CHECKING, cast

from fastapi import FastAPI

from search.application.common.application_error import ApplicationError
from search.domain.common.domain_errors import DomainError
from search.infrastructure.common.infrastructure_errors import InfrastructureError
from search.presentation.web.exceptions.handlers import (
    application_error_handler,
    domain_error_handler,
    internal_error_handler,
)

if TYPE_CHECKING:
    from starlette.types import HTTPExceptionHandler


def setup_application_error_handler(application: FastAPI) -> None:
    """Register application-level exception handlers for FastAPI."""
    application.add_exception_handler(
        ApplicationError, cast("HTTPExceptionHandler", application_error_handler)
    )


def setup_domain_error_handler(application: FastAPI) -> None:
    """Register domain-level exception handlers for FastAPI."""
    application.add_exception_handler(
        DomainError, cast("HTTPExceptionHandler", domain_error_handler)
    )


def setup_internal_error_handler(application: FastAPI) -> None:
    """Register infrastructure and base-level exception handlers for FastAPI."""
    application.add_exception_handler(
        InfrastructureError, cast("HTTPExceptionHandler", internal_error_handler)
    )
    application.add_exception_handler(
        Exception, cast("HTTPExceptionHandler", internal_error_handler)
    )
