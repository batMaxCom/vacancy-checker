import uuid
from decimal import Decimal
from typing import Annotated, Any

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body, Query
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from vacancy.application.common.dto import PaginationDto, VacancyDto
from vacancy.application.operations.commands.vacancy.create_vacancy import CreateVacancyCommand
from vacancy.application.operations.commands.vacancy.delete_vacancy import (
    DeleteVacancyByProfileIdCommand,
)
from vacancy.application.operations.commands.vacancy.update_vacancy import UpdateVacancyCommand
from vacancy.application.operations.queries.vacancy.get_vacancy_by_id import GetVacancyByIdQuery
from vacancy.application.operations.queries.vacancy.get_vacancy_by_paginated import (
    GetVacancyByPaginatedQuery,
)
from vacancy.application.ports.auth import AuthenticateProcessor
from vacancy.application.ports.cqrs import Sender
from vacancy.domain.vacancies.enums import EmploymentType, VacancyStatus, WorkFormat
from vacancy.domain.vacancies.value_objects import ProfileId, Salary, VacancyId
from vacancy.entrypoint.web.config import AppConfig
from vacancy.presentation.web.schemas.base import SuccessfulResponse
from vacancy.presentation.web.schemas.request import CreateVacancyRequest, UpdateVacancyRequest

VACANCY_CONTROLLER = APIRouter(prefix="/vacancy", tags=["Vacancy"])


@VACANCY_CONTROLLER.get("/{vacancy_id}")
@inject
async def get_vacancy_by_id(
    vacancy_id: uuid.UUID,
    *,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[VacancyDto | None]:
    await auth_processor.process()
    query = GetVacancyByIdQuery(vacancy_id=VacancyId(vacancy_id))
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@VACANCY_CONTROLLER.get("/list/paginated")
@inject
async def get_vacancy_paginated(
    page_number: Annotated[int | None, Query()] = None,
    page_size: Annotated[int | None, Query()] = None,
    profile_id: Annotated[uuid.UUID | None, Query()] = None,
    status: Annotated[list[str] | None, Query()] = None,
    *,
    sender: FromDishka[Sender],
    config: FromDishka[AppConfig],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse:
    await auth_processor.process()
    filters: dict[str, Any] = {}
    if profile_id is not None:
        filters["profile_id"] = ProfileId(profile_id)
    if status is not None:
        filters["status__in"] = status
    query = GetVacancyByPaginatedQuery(
        pagination=PaginationDto(
            page_number=page_number if page_number is not None else config.page_number,
            page_size=page_size if page_size is not None else config.page_size,
        ),
        filters=filters,
    )
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@VACANCY_CONTROLLER.post("")
@inject
async def create_vacancy(
    body: Annotated[CreateVacancyRequest, Body(embed=True)],
    *,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[None]:
    await auth_processor.process()
    salary: Salary | None = None
    if body.salary_min_amount is not None or body.salary_max_amount is not None:
        salary = Salary(
            min_amount=(
                Decimal(str(body.salary_min_amount))
                if body.salary_min_amount is not None
                else None
            ),
            max_amount=(
                Decimal(str(body.salary_max_amount))
                if body.salary_max_amount is not None
                else None
            ),
        )

    command = CreateVacancyCommand(
        vacancy_id=VacancyId(body.vacancy_id),
        profile_id=ProfileId(body.profile_id),
        external_id=body.external_id,
        title=body.title,
        description=body.description,
        company_name=body.company_name or "",
        employment_type=EmploymentType(body.employment_type),
        work_format=WorkFormat(body.work_format),
        salary=salary,
        location=body.location,
        url=body.url,
        published_at=body.published_at,
        source=body.source,
        source_url=body.source_url
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_201_CREATED)


@VACANCY_CONTROLLER.put("/{vacancy_id}")
@inject
async def update_vacancy(
    vacancy_id: uuid.UUID,
    body: Annotated[UpdateVacancyRequest, Body(embed=True)],
    *,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[None]:
    await auth_processor.process()
    salary: Salary | None = None
    if body.salary_min_amount is not None or body.salary_max_amount is not None:
        salary = Salary(
            min_amount=(
                Decimal(str(body.salary_min_amount))
                if body.salary_min_amount is not None
                else None
            ),
            max_amount=(
                Decimal(str(body.salary_max_amount))
                if body.salary_max_amount is not None
                else None
            ),
        )

    command = UpdateVacancyCommand(
        vacancy_id=VacancyId(vacancy_id),
        title=body.title,
        description=body.description,
        company_name=body.company_name,
        employment_type=EmploymentType(body.employment_type) if body.employment_type else None,
        work_format=WorkFormat(body.work_format) if body.work_format else None,
        salary=salary,
        location=body.location,
        url=body.url,
        status=VacancyStatus[body.status] if body.status else None,
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)


@VACANCY_CONTROLLER.delete("/profile/{profile_id}")
@inject
async def delete_vacancy_by_profile_id(
    profile_id: uuid.UUID,
    *,
    sender: FromDishka[Sender],
    auth_processor: FromDishka[AuthenticateProcessor]
) -> SuccessfulResponse[None]:
    await auth_processor.process()
    command = DeleteVacancyByProfileIdCommand(profile_id=ProfileId(profile_id))
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)
