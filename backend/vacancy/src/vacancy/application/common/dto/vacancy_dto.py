from dataclasses import dataclass
from datetime import datetime

from vacancy.domain.sources.value_objects import SourceId
from vacancy.domain.vacancies.enums import VacancyStatus
from vacancy.domain.vacancies.value_objects import Salary, VacancyId


@dataclass(frozen=True, slots=True)
class VacancyDto:
    vacancy_id: VacancyId
    source_id: SourceId
    external_id: str | None
    title: str
    description: str
    company_name: str | None
    employment_type: str | None
    work_format: str | None
    salary: Salary | None
    location: str | None
    url: str
    published_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None
    status: VacancyStatus
