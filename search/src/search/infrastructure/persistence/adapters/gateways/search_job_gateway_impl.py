from sqlalchemy.ext.asyncio import AsyncSession

from search.application.common.dto.search_job_dto import SearchJobDto
from search.application.ports.gateways import SearchJobGateway
from search.domain.search_job.value_objects import SearchJobId, SearchJobStatus
from search.domain.search_profile.value_objects import SearchProfileId
from search.infrastructure.persistence.adapters.common.mixins import FilterMixin, QueryMixin
from search.infrastructure.persistence.tables import SEARCH_JOB_TABLE


class SearchJobGatewayImpl(QueryMixin, FilterMixin, SearchJobGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def get_by_id(self, search_job_id: SearchJobId) -> SearchJobDto | None:
        query = self._get_query(SEARCH_JOB_TABLE)
        query = self._add_filters(SEARCH_JOB_TABLE, query, id=search_job_id)
        result = await self.__session.execute(query)
        row = result.one_or_none()
        if not row:
            return None
        return SearchJobDto(
            id=SearchJobId(row.id),
            profile_id=SearchProfileId(row.profile_id),
            started_at=row.started_at,
            finished_at=row.finished_at,
            status=SearchJobStatus(row.status),
            vacancies_found=row.vacancies_found,
        )

    async def get_by_profile_id(self, profile_id: SearchProfileId) -> list[SearchJobDto]:
        query = self._get_query(SEARCH_JOB_TABLE)
        query = self._add_filters(SEARCH_JOB_TABLE, query, profile_id=profile_id)
        result = await self.__session.execute(query)
        rows = result.all()
        return [
            SearchJobDto(
                id=SearchJobId(row.id),
                profile_id=SearchProfileId(row.profile_id),
                started_at=row.started_at,
                finished_at=row.finished_at,
                status=SearchJobStatus(row.status),
                vacancies_found=row.vacancies_found,
            )
            for row in rows
        ]
