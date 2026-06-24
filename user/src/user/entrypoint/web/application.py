from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, cast

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from user import version
from user.entrypoint.di.containers import web_container
from user.entrypoint.web.config import AppConfig, get_web_config
from user.infrastructure.adapters.logger import setup_logging
from user.infrastructure.persistence.tables import setup_mapping
from user.presentation.web.controllers import HEALTHCHECK_CONTROLLER, USER_CONTROLLER
from user.presentation.web.exceptions.setup import (
    setup_application_error_handler,
    setup_domain_error_handler,
    setup_internal_error_handler,
)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Application dependencies."""
    setup_mapping()
    container = cast(AsyncContainer, application.state.dishka_container)
    try:
        yield
    finally:
        await container.close()

def custom_openapi(application: FastAPI) -> Any:
    """Create custom OpenAPI schema."""
    if application.openapi_schema:
        return application.openapi_schema
    openapi_schema = get_openapi(
        title="Users",
        version=f"{version}",
        summary="User API manager",
        routes=application.routes
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    application.openapi_schema = openapi_schema
    return application.openapi_schema

def setup_application(config: AppConfig) -> FastAPI:
    application = FastAPI(
        lifespan=lifespan,
        openapi_url=config.open_api_schema_path,
        docs_url=config.docs_path,
        swagger_ui_parameters={
            "displayRequestDuration": True,
            "persistAuthorization": True,
        }
    )
    application.openapi = lambda: custom_openapi(application)  # type: ignore[method-assign]
    return application

def setup_exception_handlers(application: FastAPI) -> None:
    """Register exception handlers for FastAPI."""
    setup_application_error_handler(application=application)
    setup_domain_error_handler(application=application)
    setup_internal_error_handler(application=application)

def setup_middleware(application: FastAPI, config: AppConfig) -> None:
    origins = ["*"] if config.debug else config.cors_origins
    application.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_controllers(application: FastAPI) -> None:
    application.include_router(HEALTHCHECK_CONTROLLER)
    application.include_router(USER_CONTROLLER)

def app_factory() -> FastAPI:
    config = get_web_config()
    setup_logging(debug=config.app_config.debug)
    container = web_container(
        app_config=config.app_config,
        db_config=config.db_config,
    )
    application = setup_application(config.app_config)
    setup_middleware(application, config.app_config)
    setup_controllers(application)
    setup_exception_handlers(application)
    setup_dishka(container=container, app=application)
    return application
