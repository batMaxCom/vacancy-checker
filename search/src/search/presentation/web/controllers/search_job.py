from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from search.application.common.dto import SearchJobDto
from search.application.operations.queries.search_job import GetSearchJobQuery
from search.application.ports.cqrs import Sender
from search.domain.search_job.value_objects import SearchJobId
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
