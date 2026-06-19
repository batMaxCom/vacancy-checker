from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class EmploymentType(Enum):
    FULL_TIME = auto()
    PART_TIME = auto()
    CONTRACT = auto()
    INTERNSHIP = auto()


class WorkFormat(Enum):
    REMOTE = auto()
    HYBRID = auto()
    OFFICE = auto()


@dataclass(frozen=True)
class Salary:
    min_amount: str | None
    max_amount: str | None


@dataclass(frozen=True)
class FoundVacancyDto:
    external_id: str
    title: str
    description: str
    company_name: str
    url: str
    source: str
    salary: Salary | None = None
    location: str | None = None
    employment_type: EmploymentType | None = None
    work_format: WorkFormat | None = None
    published_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def to_dict(self) -> dict:
        d: dict[str, object] = {}
        for field_name in (
            "external_id",
            "title",
            "description",
            "company_name",
            "url",
            "source",
            "location",
        ):
            d[field_name] = getattr(self, field_name)
        salary = self.salary
        if salary is not None:
            d["salary"] = {
                "min_amount": salary.min_amount,
                "max_amount": salary.max_amount,
            }
        else:
            d["salary"] = None
        et = self.employment_type
        d["employment_type"] = et.name if et is not None else None
        wf = self.work_format
        d["work_format"] = wf.name if wf is not None else None
        for field_name in ("published_at", "created_at", "updated_at"):
            val = getattr(self, field_name)
            d[field_name] = val.isoformat() if val is not None else None
        return d
