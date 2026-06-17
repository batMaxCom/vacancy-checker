from dataclasses import dataclass

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from search.presentation.web.schemas.base import SuccessfulResponse

HEALTHCHECK_CONTROLLER = APIRouter()

@dataclass(frozen=True)
class Healthcheck:
    status: str


@HEALTHCHECK_CONTROLLER.get("/healthcheck", include_in_schema=False)
def healthcheck() -> SuccessfulResponse[Healthcheck]:
    return SuccessfulResponse(status_code=HTTP_200_OK, result=Healthcheck("OK"))
