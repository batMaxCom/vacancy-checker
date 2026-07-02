from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from starlette.status import HTTP_200_OK

from auth.application.ports.auth import AuthServicePort
from auth.presentation.web.schemas.base import SuccessfulResponse
from auth.presentation.web.schemas.request import LoginRequest, LogoutRequest, RefreshTokenRequest

AUTH_CONTROLLER = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@AUTH_CONTROLLER.post("/login")
@inject
async def login(
    body: LoginRequest,
    *,
    auth_service: FromDishka[AuthServicePort],
) -> SuccessfulResponse[dict]:
    result = await auth_service.login(email=body.email, password=body.password)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@AUTH_CONTROLLER.post("/refresh")
@inject
async def refresh(
    body: RefreshTokenRequest,
    *,
    auth_service: FromDishka[AuthServicePort],
) -> SuccessfulResponse[dict]:
    result = await auth_service.refresh(refresh_token=body.refresh_token)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@AUTH_CONTROLLER.post("/logout")
@inject
async def logout(
    user_id: Annotated[str, Query()],
    body: LogoutRequest,
    *,
    auth_service: FromDishka[AuthServicePort],
) -> SuccessfulResponse[None]:
    await auth_service.logout(user_id=user_id, refresh_token=body.refresh_token)
    return SuccessfulResponse(status_code=HTTP_200_OK)
