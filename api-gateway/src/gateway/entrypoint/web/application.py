from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from gateway.entrypoint.web.config import GatewayConfig, get_gateway_config
from gateway.presentation.web.controllers import (
    HEALTHCHECK_CONTROLLER,
    PROXY_CONTROLLER,
    setup_proxy_routes,
)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    yield


def custom_openapi(application: FastAPI) -> Any:
    if application.openapi_schema:
        return application.openapi_schema
    openapi_schema = get_openapi(
        title="API Gateway",
        version="0.1.0",
        summary="Unified entry point for all microservices",
        routes=application.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
    }
    application.openapi_schema = openapi_schema
    return application.openapi_schema


def setup_application(config: GatewayConfig) -> FastAPI:
    application = FastAPI(
        lifespan=lifespan,
        openapi_url="/openapi.json",
        docs_url="/docs",
        swagger_ui_parameters={
            "displayRequestDuration": True,
            "persistAuthorization": True,
        },
    )
    application.state.config = config
    application.openapi = lambda: custom_openapi(application)
    return application


def setup_middleware(application: FastAPI, config: GatewayConfig) -> None:
    origins = ["*"] if config.debug else ["*"]
    application.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_controllers(application: FastAPI) -> None:
    config: GatewayConfig = application.state.config
    upstream_map = {
        "auth_url": config.auth_url,
        "user_url": config.user_url,
        "search_url": config.search_url,
        "vacancy_url": config.vacancy_url,
    }
    application.include_router(HEALTHCHECK_CONTROLLER)
    setup_proxy_routes(PROXY_CONTROLLER, upstream_map)
    application.include_router(PROXY_CONTROLLER)


def app_factory() -> FastAPI:
    config = get_gateway_config()
    application = setup_application(config)
    setup_middleware(application, config)
    setup_controllers(application)
    return application
