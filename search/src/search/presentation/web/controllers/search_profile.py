from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from search.application.common.dto import (
    SearchJobDto,
    SearchProfileDto,
    SelectSearchProfileDto,
)
from search.application.operations.commands.search_job import RunSearchCommand
from search.application.operations.commands.search_profile import (
    ActivateSearchProfileCommand,
    CreateSearchProfileCommand,
    DeactivateSearchProfileCommand,
    DeleteSearchProfileCommand,
    UpdateSearchProfileCommand,
)
from search.application.operations.queries.search_job import GetProfileJobsQuery
from search.application.operations.queries.search_profile import (
    GetSearchProfileQuery,
    GetUserSearchProfilesQuery,
    GetUserSearchProfilesSelectQuery,
)
from search.application.ports.auth import AuthenticateProcessor
from search.application.ports.cqrs import Sender
from search.domain.search_job.value_objects import SearchJobId
from search.domain.search_profile.value_objects import SearchProfileId
from search.presentation.web.schemas import (
    CreateSearchProfileRequest,
    SuccessfulResponse,
    UpdateSearchProfileRequest,
)

SEARCH_PROFILE_CONTROLLER = APIRouter(
    prefix="/search-profiles", tags=["Search Profiles"],
)


@SEARCH_PROFILE_CONTROLLER.post("")
@inject
async def create_search_profile(
    body: CreateSearchProfileRequest,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[SearchProfileId]:
    await auth_processor.process()
    command = CreateSearchProfileCommand(
        name=body.name,
        keywords=body.keywords,
        search_interval_minutes=body.search_interval_minutes,
    )
    result = await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_201_CREATED, result=result)


@SEARCH_PROFILE_CONTROLLER.get("")
@inject
async def get_user_search_profiles(
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[list[SearchProfileDto]]:
    await auth_processor.process()
    query = GetUserSearchProfilesQuery()
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@SEARCH_PROFILE_CONTROLLER.get("/select")
@inject
async def get_user_search_profiles_select(
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[list[SelectSearchProfileDto]]:
    await auth_processor.process()
    query = GetUserSearchProfilesSelectQuery()
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@SEARCH_PROFILE_CONTROLLER.get("/{profile_id}")
@inject
async def get_search_profile_by_id(
    profile_id: UUID,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[SearchProfileDto | None]:
    await auth_processor.process()
    query = GetSearchProfileQuery(
        search_profile_id=SearchProfileId(profile_id),
    )
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@SEARCH_PROFILE_CONTROLLER.patch("/{profile_id}")
@inject
async def update_search_profile(
    profile_id: UUID,
    body: UpdateSearchProfileRequest,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[None]:
    await auth_processor.process()
    command = UpdateSearchProfileCommand(
        search_profile_id=SearchProfileId(profile_id),
        name=body.name,
        keywords=body.keywords,
        search_interval_minutes=body.search_interval_minutes,
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)


@SEARCH_PROFILE_CONTROLLER.delete("/{profile_id}")
@inject
async def delete_search_profile(
    profile_id: UUID,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[None]:
    await auth_processor.process()
    command = DeleteSearchProfileCommand(
        search_profile_id=SearchProfileId(profile_id),
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)


@SEARCH_PROFILE_CONTROLLER.post("/{profile_id}/activate")
@inject
async def activate_search_profile(
    profile_id: UUID,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[None]:
    await auth_processor.process()
    command = ActivateSearchProfileCommand(
        search_profile_id=SearchProfileId(profile_id),
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)


@SEARCH_PROFILE_CONTROLLER.post("/{profile_id}/deactivate")
@inject
async def deactivate_search_profile(
    profile_id: UUID,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[None]:
    await auth_processor.process()
    command = DeactivateSearchProfileCommand(
        search_profile_id=SearchProfileId(profile_id),
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)


@SEARCH_PROFILE_CONTROLLER.post("/{profile_id}/search")
@inject
async def run_search(
    profile_id: UUID,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[SearchJobId]:
    await auth_processor.process()
    command = RunSearchCommand(profile_id=SearchProfileId(profile_id))
    result = await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_201_CREATED, result=result)


@SEARCH_PROFILE_CONTROLLER.get("/{profile_id}/jobs")
@inject
async def get_profile_jobs(
    profile_id: UUID,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[list[SearchJobDto]]:
    await auth_processor.process()
    query = GetProfileJobsQuery(profile_id=SearchProfileId(profile_id))
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)
