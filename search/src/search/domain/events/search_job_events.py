from dataclasses import dataclass, field
from datetime import datetime, timezone

from search.domain.events.base_event import DomainEvent
from search.domain.search_job.value_objects import SearchJobId
from search.domain.search_profile.value_objects import SearchProfileId


@dataclass(frozen=True, slots=True)
class SearchStarted(DomainEvent):
    job_id: SearchJobId
    profile_id: SearchProfileId


@dataclass(frozen=True, slots=True)
class SearchCompleted(DomainEvent):
    job_id: SearchJobId
    profile_id: SearchProfileId
    vacancies_found: int


@dataclass(frozen=True, slots=True)
class VacancyData:
    external_id: str
    title: str
    description: str
    url: str
    company: str


@dataclass(frozen=True, slots=True)
class VacancyFound(DomainEvent):
    profile_id: SearchProfileId
    user_id: str
    vacancy: VacancyData = field(default_factory=lambda: VacancyData(
        external_id="",
        title="",
        description="",
        url="",
        company="",
    ))


def search_started(
    job_id: SearchJobId,
    profile_id: SearchProfileId,
    occurred_at: datetime | None = None,
) -> SearchStarted:
    return SearchStarted(
        job_id=job_id,
        profile_id=profile_id,
        occurred_at=occurred_at or datetime.now(tz=timezone.utc),
    )


def search_completed(
    job_id: SearchJobId,
    profile_id: SearchProfileId,
    vacancies_found: int,
    occurred_at: datetime | None = None,
) -> SearchCompleted:
    return SearchCompleted(
        job_id=job_id,
        profile_id=profile_id,
        vacancies_found=vacancies_found,
        occurred_at=occurred_at or datetime.now(tz=timezone.utc),
    )
