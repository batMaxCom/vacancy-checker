from dataclasses import dataclass


@dataclass(frozen=True)
class FoundVacancyDto:
    external_id: str
    title: str
    description: str
    company: str
    url: str
    source: str
