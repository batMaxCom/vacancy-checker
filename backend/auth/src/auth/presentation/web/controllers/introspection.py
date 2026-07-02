
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from auth.application.ports.auth import AuthContext, AuthenticationPort
from auth.presentation.web.schemas.base import SuccessfulResponse

INTROSPECTION_CONTROLLER = APIRouter(prefix="/api/v1/internal/auth", tags=["internal"], include_in_schema=False)


@INTROSPECTION_CONTROLLER.get("/introspect")
@inject
async def introspect(
    authentication: FromDishka[AuthenticationPort],
) -> SuccessfulResponse[AuthContext]:
    result = await authentication.authenticate()
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)
