import uuid
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body, Query
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from vacancy.application.common.dto import PaginationDto, SelectItemDto, SourceDto
from vacancy.application.operations.commands.source.create_source import CreateSourceCommand
from vacancy.application.operations.commands.source.update_source import UpdateSourceCommand
from vacancy.application.operations.queries.source.get_source_by_id import GetSourceByIdQuery
from vacancy.application.operations.queries.source.get_source_by_paginated import (
    GetSourceByPaginatedQuery,
)
from vacancy.application.operations.queries.source.get_source_by_select_list import (
    GetSourceBySelectListQuery,
)
from vacancy.application.ports.cqrs import Sender
from vacancy.domain.sources.value_objects import SourceId
from vacancy.entrypoint.web.config import AppConfig
from vacancy.presentation.web.schemas.base import SuccessfulResponse
from vacancy.presentation.web.schemas.request import CreateSourceRequest, UpdateSourceRequest

SOURCE_CONTROLLER = APIRouter(prefix="/source", tags=["source"])


@SOURCE_CONTROLLER.get("/{source_id}")
@inject
async def get_source_by_id(
    source_id: uuid.UUID,
    sender: FromDishka[Sender],
) -> SuccessfulResponse[SourceDto | None]:
    query = GetSourceByIdQuery(source_id=SourceId(source_id))
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@SOURCE_CONTROLLER.get("/list/paginated")
@inject
async def get_source_paginated(
    sender: FromDishka[Sender],
    config: FromDishka[AppConfig],
    page_number: Annotated[int | None, Query()] = None,
    page_size: Annotated[int | None, Query()] = None,
) -> SuccessfulResponse:
    query = GetSourceByPaginatedQuery(
        pagination=PaginationDto(
            page_number=page_number if page_number is not None else config.page_number,
            page_size=page_size if page_size is not None else config.page_size,
        ),
    )
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@SOURCE_CONTROLLER.get("/list/select")
@inject
async def get_source_select_list(
    sender: FromDishka[Sender],
) -> SuccessfulResponse[list[SelectItemDto[SourceId]]]:
    query = GetSourceBySelectListQuery()
    result = await sender.send(query)
    return SuccessfulResponse(status_code=HTTP_200_OK, result=result)


@SOURCE_CONTROLLER.post("")
@inject
async def create_source(
    body: Annotated[CreateSourceRequest, Body(embed=True)],
    sender: FromDishka[Sender],
) -> SuccessfulResponse[None]:
    command = CreateSourceCommand(name=body.name, base_url=body.base_url)
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_201_CREATED)


@SOURCE_CONTROLLER.put("/{source_id}")
@inject
async def update_source(
    source_id: uuid.UUID,
    body: Annotated[UpdateSourceRequest, Body(embed=True)],
    sender: FromDishka[Sender],
) -> SuccessfulResponse[None]:
    command = UpdateSourceCommand(
        source_id=SourceId(source_id),
        name=body.name,
        base_url=body.base_url,
        is_active=body.is_active,
    )
    await sender.send(command)
    return SuccessfulResponse(status_code=HTTP_200_OK)
