from decimal import Decimal
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from vacancy.application.common.dto import PaginationDto, PaginationResultDto, VacancyDto
from vacancy.application.ports.gateways import VacancyGateway
from vacancy.domain.sources.value_objects import SourceId
from vacancy.domain.vacancies.enums import EmploymentType, VacancyStatus, WorkFormat
from vacancy.domain.vacancies.value_objects import Salary, VacancyId
from vacancy.infrastructure.persistence.adapters.common.mixins import FilterMixin, PaginationMixin
from vacancy.infrastructure.persistence.tables.vacancy import VACANCY_TABLE


class VacancyGatewayImpl(VacancyGateway, FilterMixin, PaginationMixin):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def get_by_id(self, vacancy_id: VacancyId) -> VacancyDto | None:
        query = select(
            VACANCY_TABLE.c.id,
            VACANCY_TABLE.c.source_id,
            VACANCY_TABLE.c.external_id,
            VACANCY_TABLE.c.title,
            VACANCY_TABLE.c.description,
            VACANCY_TABLE.c.company_name,
            VACANCY_TABLE.c.employment_type,
            VACANCY_TABLE.c.work_format,
            VACANCY_TABLE.c.salary_min_amount,
            VACANCY_TABLE.c.salary_max_amount,
            VACANCY_TABLE.c.location,
            VACANCY_TABLE.c.url,
            VACANCY_TABLE.c.published_at,
            VACANCY_TABLE.c.created_at,
            VACANCY_TABLE.c.updated_at,
            VACANCY_TABLE.c.status,
        ).where(VACANCY_TABLE.c.id == vacancy_id)

        result = await self.__session.execute(query)
        row = result.one_or_none()
        if row is None:
            return None

        return self._row_to_dto(row)

    async def get_paginated(
        self,
        pagination: PaginationDto,
        **filters: Any,
    ) -> PaginationResultDto[VacancyDto]:
        base_query = select(
            VACANCY_TABLE.c.id,
            VACANCY_TABLE.c.source_id,
            VACANCY_TABLE.c.external_id,
            VACANCY_TABLE.c.title,
            VACANCY_TABLE.c.description,
            VACANCY_TABLE.c.company_name,
            VACANCY_TABLE.c.employment_type,
            VACANCY_TABLE.c.work_format,
            VACANCY_TABLE.c.salary_min_amount,
            VACANCY_TABLE.c.salary_max_amount,
            VACANCY_TABLE.c.location,
            VACANCY_TABLE.c.url,
            VACANCY_TABLE.c.published_at,
            VACANCY_TABLE.c.created_at,
            VACANCY_TABLE.c.updated_at,
            VACANCY_TABLE.c.status,
        )
        base_query = self._add_filters(VACANCY_TABLE, base_query, **filters)

        count_query = select(func.count()).select_from(VACANCY_TABLE)
        count_query = self._add_filters(VACANCY_TABLE, count_query, **filters)
        count_result = await self.__session.execute(count_query)
        count_records = count_result.scalar() or 0

        base_query = self._add_query_offset_and_limit(
            base_query, pagination.page_number, pagination.page_size
        )

        result = await self.__session.execute(base_query)
        rows = result.all()

        records = [self._row_to_dto(row) for row in rows]

        return self._get_pagination_result(pagination, records, count_records)

    @staticmethod
    def _row_to_dto(row: Any) -> VacancyDto:
        salary: Salary | None = None
        if row.salary_min_amount is not None or row.salary_max_amount is not None:
            min_amount = (
                Decimal(row.salary_min_amount) if row.salary_min_amount is not None else None
            )
            max_amount = (
                Decimal(row.salary_max_amount) if row.salary_max_amount is not None else None
            )
            salary = Salary(min_amount=min_amount, max_amount=max_amount)

        return VacancyDto(
            vacancy_id=VacancyId(row.id),
            source_id=SourceId(row.source_id),
            external_id=row.external_id,
            title=row.title,
            description=row.description,
            company_name=row.company_name,
            employment_type=EmploymentType(row.employment_type),
            work_format=WorkFormat(row.work_format),
            salary=salary,
            location=row.location,
            url=row.url,
            published_at=row.published_at,
            created_at=row.created_at,
            updated_at=row.updated_at,
            status=VacancyStatus(row.status),
        )
