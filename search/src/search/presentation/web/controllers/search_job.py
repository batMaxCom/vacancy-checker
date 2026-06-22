from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from search.application.common.dto import SearchJobDto
from search.application.operations.commands.search_job import (
    DeleteSearchJobsByProfileIdCommand,
)
from search.application.operations.queries.search_job import GetSearchJobQuery
from search.application.ports.cqrs import Sender
from search.domain.search_job.value_objects import SearchJobId
from search.domain.search_profile.value_objects import SearchProfileId
from search.presentation.web.schemas.base import SuccessfulResponse

SEARCH_JOB_CONTROLLER = APIRouter(
    prefix="/api/v1/search-jobs", tags=["search-jobs"],
)


@SEARCH_JOB_CONTROLLER.get("/{job_id}")
@inject
async def get_search_job_by_id(
    job_id: UUID,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[SearchJobDto | None]:
    query = GetSearchJobQuery(search_job_id=SearchJobId(job_id))
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@SEARCH_JOB_CONTROLLER.delete("/profile/{profile_id}")
@inject
async def delete_search_jobs_by_profile_id(
    profile_id: UUID,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[None]:
    command = DeleteSearchJobsByProfileIdCommand(
        profile_id=SearchProfileId(profile_id),
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)
