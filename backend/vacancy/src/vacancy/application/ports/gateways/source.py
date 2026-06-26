from abc import ABC, abstractmethod
from typing import Any

from vacancy.application.common.dto import (
    PaginationDto,
    PaginationResultDto,
    SelectItemDto,
    SourceDto,
)
from vacancy.domain.sources.value_objects import SourceId


class SourceGateway(ABC):

    @abstractmethod
    async def get_by_id(
        self,
        source_id: SourceId,
    ) -> SourceDto | None:
        """Get source by id."""

    @abstractmethod
    async def get_paginated(
            self,
            pagination: PaginationDto,
            **filters: Any
    ) -> PaginationResultDto[SourceDto]:
        """Get paginated source"""

    @abstractmethod
    async def get_select_list(
        self,
    ) -> list[SelectItemDto[SourceId]]:
        """Get source select list."""
