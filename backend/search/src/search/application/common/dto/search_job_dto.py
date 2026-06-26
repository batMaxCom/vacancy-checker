from dataclasses import dataclass
from datetime import datetime

from search.domain.search_job.value_objects import SearchJobId, SearchJobStatus
from search.domain.search_profile.value_objects import SearchProfileId


@dataclass(frozen=True, slots=True)
class SearchJobDto:
    id: SearchJobId
    profile_id: SearchProfileId
    started_at: datetime
    finished_at: datetime | None
    status: SearchJobStatus
    vacancies_found: int
