from abc import ABC, abstractmethod
from typing import Any

from user.application.common.dto import Pagination, PaginationResult, UserBriefDTO


class UserGateway(ABC):

    @abstractmethod
    async def get_paginated(
        self,
        pagination: Pagination,
        **filters: Any,
    ) -> PaginationResult[UserBriefDTO]:
        """Get paginated users."""
