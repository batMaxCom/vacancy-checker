from datetime import datetime, timezone

from search.domain.ports import Entity
from search.domain.search_job.value_objects import SearchJobId, SearchJobStatus
from search.domain.search_profile.value_objects import SearchProfileId


class SearchJob(Entity[SearchJobId]):
    def __init__(
        self,
        search_job_id: SearchJobId,
        profile_id: SearchProfileId,
        started_at: datetime,
        finished_at: datetime | None = None,
        status: SearchJobStatus = SearchJobStatus.PENDING,
        vacancies_found: int = 0,
    ) -> None:
        super().__init__(search_job_id)
        self._profile_id = profile_id
        self._started_at = started_at
        self._finished_at = finished_at
        self._status = status
        self._vacancies_found = vacancies_found

    @property
    def profile_id(self) -> SearchProfileId:
        return self._profile_id

    @property
    def started_at(self) -> datetime:
        return self._started_at

    @property
    def finished_at(self) -> datetime | None:
        return self._finished_at

    @property
    def status(self) -> SearchJobStatus:
        return self._status

    @property
    def vacancies_found(self) -> int:
        return self._vacancies_found

    def start(self) -> None:
        self._status = SearchJobStatus.RUNNING

    def complete(self, vacancies_found: int) -> None:
        self._status = SearchJobStatus.SUCCESS
        self._finished_at = datetime.now(tz=timezone.utc)
        self._vacancies_found = vacancies_found

    def fail(self) -> None:
        self._status = SearchJobStatus.FAILED
        self._finished_at = datetime.now(tz=timezone.utc)

    def retry(self) -> None:
        self._status = SearchJobStatus.PENDING
        self._finished_at = None
