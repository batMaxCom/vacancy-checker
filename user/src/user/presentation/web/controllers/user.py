import uuid
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body, Query
from starlette.status import HTTP_200_OK

from user.application.common.dto import Pagination, PaginationResult, UserBriefDTO, UserDTO
from user.application.operations.commands.user import (
    ActivateUserCommand,
    ChangeRoleCommand,
    DeleteUserCommand,
    SuspendUserCommand,
    UpdateProfileCommand,
)
from user.application.operations.queries.user import (
    GetCurrentUserQuery,
    GetUserByIdQuery,
    GetUsersQuery,
)
from user.application.ports.cqrs import Sender
from user.domain.user.value_objects import AvatarUrl, FirstName, LastName, UserId, UserRole
from user.presentation.web.schemas.base import SuccessfulResponse
from user.presentation.web.schemas.request import (
    ChangeRoleRequest,
    UpdateProfileRequest,
)

USER_CONTROLLER = APIRouter(prefix="/user", tags=["user"])


@USER_CONTROLLER.get("/me")
@inject
async def get_current_user(
    user_id: Annotated[uuid.UUID, Query()],
    *,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[UserDTO | None]:
    query = GetCurrentUserQuery(user_id=UserId(user_id))
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@USER_CONTROLLER.get("/list/paginated")
@inject
async def get_users_paginated(
    page_number: Annotated[int, Query()] = 1,
    page_size: Annotated[int, Query()] = 20,
    role: Annotated[str | None, Query()] = None,
    status: Annotated[str | None, Query()] = None,
    *,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[PaginationResult[UserBriefDTO]]:
    query = GetUsersQuery(
        pagination=Pagination(page_number=page_number, page_size=page_size),
        role=role,
        status=status,
    )
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@USER_CONTROLLER.get("/{user_id}")
@inject
async def get_user_by_id(
    user_id: uuid.UUID,
    *,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[UserBriefDTO | None]:
    query = GetUserByIdQuery(user_id=UserId(user_id))
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


# @USER_CONTROLLER.post("")
# @inject
# async def create_user(
#     body: Annotated[CreateUserRequest, Body(embed=True)],
#     *,
#     sender: FromDishka[Sender],
# ) -> SuccessfulResponse[None]:
#     command = CreateUserCommand(
#         user_id=UserId(uuid.uuid4()),
#         email=Email(body.email),
#         first_name=FirstName(body.first_name),
#         last_name=LastName(body.last_name),
#     )
#     await sender.send(command)
#     return SuccessfulResponse(status_code=HTTP_201_CREATED)


@USER_CONTROLLER.patch("/{user_id}/profile")
@inject
async def update_profile(
    user_id: uuid.UUID,
    body: Annotated[UpdateProfileRequest, Body(embed=True)],
    *,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[None]:
    command = UpdateProfileCommand(
        user_id=UserId(user_id),
        first_name=FirstName(body.first_name),
        last_name=LastName(body.last_name),
        avatar_url=AvatarUrl(body.avatar_url) if body.avatar_url is not None else None,
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)


@USER_CONTROLLER.patch("/{user_id}/role")
@inject
async def change_role(
    user_id: uuid.UUID,
    body: Annotated[ChangeRoleRequest, Body(embed=True)],
    *,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[None]:
    command = ChangeRoleCommand(
        user_id=UserId(user_id),
        role=UserRole[body.role],
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)


@USER_CONTROLLER.post("/{user_id}/activate")
@inject
async def activate_user(
    user_id: uuid.UUID,
    *,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[None]:
    command = ActivateUserCommand(user_id=UserId(user_id))
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)


@USER_CONTROLLER.post("/{user_id}/suspend")
@inject
async def suspend_user(
    user_id: uuid.UUID,
    *,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[None]:
    command = SuspendUserCommand(user_id=UserId(user_id))
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)


@USER_CONTROLLER.delete("/{user_id}")
@inject
async def delete_user(
    user_id: uuid.UUID,
    *,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[None]:
    command = DeleteUserCommand(user_id=UserId(user_id))
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)
