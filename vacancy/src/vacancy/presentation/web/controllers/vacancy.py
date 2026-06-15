from datetime import datetime
from decimal import Decimal

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from vacancy.application.common.dto import PaginationDto, VacancyDto
from vacancy.application.operations.commands.vacancy.create_vacancy import CreateVacancyCommand
from vacancy.application.operations.commands.vacancy.update_vacancy import UpdateVacancyCommand
from vacancy.application.operations.queries.vacancy.get_vacancy_by_id import GetVacancyByIdQuery
from vacancy.application.operations.queries.vacancy.get_vacancy_by_paginated import (
    GetVacancyByPaginatedQuery,
)
from vacancy.application.ports.cqrs import Sender
from vacancy.domain.sources.value_objects import SourceId
from vacancy.domain.vacancies.enums import EmploymentType, VacancyStatus, WorkFormat
from vacancy.domain.vacancies.value_objects import Salary, VacancyId
from vacancy.presentation.web.schemas.base import SuccessfulResponse

VACANCY_CONTROLLER = APIRouter(prefix="/vacancy", tags=["vacancy"])


@VACANCY_CONTROLLER.get("/{vacancy_id}")
@inject
async def get_vacancy_by_id(
    vacancy_id: int,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[VacancyDto | None]:
    query = GetVacancyByIdQuery(vacancy_id=VacancyId(vacancy_id))
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@VACANCY_CONTROLLER.get("/list/paginated")
@inject
async def get_vacancy_paginated(
    page_number: int,
    page_size: int,
    sender: FromDishka[Sender],
) -> SuccessfulResponse:
    query = GetVacancyByPaginatedQuery(
        pagination=PaginationDto(page_number=page_number, page_size=page_size),
    )
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@VACANCY_CONTROLLER.post("")
@inject
async def create_vacancy(
    vacancy_id: int,
    source_id: int,
    external_id: str,
    title: str,
    description: str,
    company_name: str | None,
    employment_type: str,
    work_format: str,
    salary_min_amount: float | None,
    salary_max_amount: float | None,
    location: str | None,
    url: str,
    published_at: datetime,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[None]:
    salary: Salary | None = None
    if salary_min_amount is not None or salary_max_amount is not None:
        salary = Salary(
            min_amount=Decimal(str(salary_min_amount)) if salary_min_amount is not None else None,
            max_amount=Decimal(str(salary_max_amount)) if salary_max_amount is not None else None,
        )

    command = CreateVacancyCommand(
        vacancy_id=VacancyId(vacancy_id),
        source_id=SourceId(source_id),
        external_id=external_id,
        title=title,
        description=description,
        company_name=company_name,
        employment_type=EmploymentType(employment_type),
        work_format=WorkFormat(work_format),
        salary=salary,
        location=location,
        url=url,
        published_at=published_at,
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_201_CREATED)


@VACANCY_CONTROLLER.put("/{vacancy_id}")
@inject
async def update_vacancy(
    vacancy_id: int,
    title: str | None,
    description: str | None,
    company_name: str | None,
    employment_type: str | None,
    work_format: str | None,
    salary_min_amount: float | None,
    salary_max_amount: float | None,
    location: str | None,
    url: str | None,
    status: str | None,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[None]:
    salary: Salary | None = None
    if salary_min_amount is not None or salary_max_amount is not None:
        salary = Salary(
            min_amount=Decimal(str(salary_min_amount)) if salary_min_amount is not None else None,
            max_amount=Decimal(str(salary_max_amount)) if salary_max_amount is not None else None,
        )

    command = UpdateVacancyCommand(
        vacancy_id=VacancyId(vacancy_id),
        title=title,
        description=description,
        company_name=company_name,
        employment_type=EmploymentType(employment_type) if employment_type else None,
        work_format=WorkFormat(work_format) if work_format else None,
        salary=salary,
        location=location,
        url=url,
        status=VacancyStatus(status) if status else None,
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)
