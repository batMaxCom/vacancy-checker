from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from user.application.common.dto import UserDTO
from user.application.operations.commands.user import (
    DeleteUserCommand,
    UpdateProfileCommand,
)
from user.application.operations.queries.user import GetCurrentUserQuery
from user.application.ports.auth import AuthenticateProcessor
from user.application.ports.cqrs import Sender
from user.domain.user.value_objects import AvatarUrl, FirstName, LastName
from user.presentation.web.schemas.base import SuccessfulResponse
from user.presentation.web.schemas.request import UpdateProfileRequest

PROFILE_CONTROLLER = APIRouter(prefix="/api/v1/profile", tags=["Profile"])


@PROFILE_CONTROLLER.get("")
@inject
async def get_current_user(
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor],
) -> SuccessfulResponse[UserDTO | None]:
    await auth_processor.process()
    query = GetCurrentUserQuery()
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@PROFILE_CONTROLLER.patch("")
@inject
async def update_current_user(
    body: UpdateProfileRequest,
    *,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[None]:
    await auth_processor.process()
    command = UpdateProfileCommand(
        first_name=FirstName(body.first_name),
        last_name=LastName(body.last_name),
        avatar_url=AvatarUrl(body.avatar_url) if body.avatar_url is not None else None,
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)


@PROFILE_CONTROLLER.delete("")
@inject
async def delete_current_user(
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[None]:
    await auth_processor.process()
    command = DeleteUserCommand()
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)
