from dataclasses import dataclass

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

HEALTHCHECK_CONTROLLER = APIRouter()


@dataclass(frozen=True)
class Healthcheck:
    status: str


@HEALTHCHECK_CONTROLLER.get("/healthcheck", include_in_schema=False)
def healthcheck() -> dict:
    return {"status": "ok"}
