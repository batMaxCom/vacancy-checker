import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateSourceRequest:
    name: str
    base_url: str = ""


@dataclass(frozen=True)
class UpdateSourceRequest:
    name: str | None = None
    base_url: str | None = None
    is_active: bool | None = None


@dataclass(frozen=True)
class CreateVacancyRequest:
    vacancy_id: uuid.UUID
    source_id: uuid.UUID
    external_id: str | None
    title: str
    description: str
    company_name: str | None
    employment_type: str
    work_format: str
    salary_min_amount: float | None
    salary_max_amount: float | None
    location: str | None
    url: str
    published_at: datetime


@dataclass(frozen=True)
class UpdateVacancyRequest:
    title: str | None = None
    description: str | None = None
    company_name: str | None = None
    employment_type: str | None = None
    work_format: str | None = None
    salary_min_amount: float | None = None
    salary_max_amount: float | None = None
    location: str | None = None
    url: str | None = None
    status: str | None = None
