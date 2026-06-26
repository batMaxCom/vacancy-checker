from abc import ABC, abstractmethod
from typing import Any

from vacancy.application.common.dto import PaginationDto, PaginationResultDto, VacancyDto
from vacancy.domain.vacancies.value_objects import VacancyId


class VacancyGateway(ABC):

    @abstractmethod
    async def get_by_id(
        self,
        vacancy_id: VacancyId,
    ) -> VacancyDto | None:
        """Get vacancy by id."""

    @abstractmethod
    async def get_paginated(
            self,
            pagination: PaginationDto,
            **filters: Any
    ) -> PaginationResultDto[VacancyDto]:
        """Get paginated models"""
