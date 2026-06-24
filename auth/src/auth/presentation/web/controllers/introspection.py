
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from auth.application.ports.auth import AuthContext, AuthenticationPort
from auth.presentation.web.schemas.base import SuccessfulResponse
from auth.presentation.web.schemas.request import IntrospectRequest

INTROSPECTION_CONTROLLER = APIRouter(prefix="/auth", tags=["auth"])


@INTROSPECTION_CONTROLLER.post("/introspect")
@inject
async def introspect(
    body: IntrospectRequest,
    *,
    authentication: FromDishka[AuthenticationPort],
) -> SuccessfulResponse[AuthContext]:
    result = await authentication.authenticate(access_token=body.access_token)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)
