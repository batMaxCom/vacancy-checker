from uuid import uuid4

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from auth.application.operations.commands.credential import CreateUserCredentialCommand
from auth.application.ports.cqrs import Sender
from auth.domain.common.value_objects import UserId
from auth.domain.credential.value_objects import Email
from auth.domain.shared_kernel.value_objects import FirstName, LastName
from auth.presentation.web.schemas.base import SuccessfulResponse
from auth.presentation.web.schemas.request import RegisterRequest

REGISTRATION_CONTROLLER = APIRouter(prefix="/auth", tags=["auth"])


@REGISTRATION_CONTROLLER.post("/register")
@inject
async def register(
    body: RegisterRequest,
    *,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[None]:
    command = CreateUserCredentialCommand(
        user_id=UserId(uuid4()),
        email=Email(body.email),
        password=body.password,
        first_name=FirstName(body.first_name),
        last_name=LastName(body.last_name),
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_201_CREATED)
