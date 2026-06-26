from dataclasses import dataclass


@dataclass(frozen=True)
class CreateSearchProfileRequest:
    name: str
    keywords: list[str]
    search_interval_minutes: int


@dataclass(frozen=True)
class UpdateSearchProfileRequest:
    name: str
    keywords: list[str]
    search_interval_minutes: int
