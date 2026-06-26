from dataclasses import dataclass


@dataclass(frozen=True)
class NewVacancy:
    external_id: str
    title: str
    description: str
    company: str
    url: str
    source: str
