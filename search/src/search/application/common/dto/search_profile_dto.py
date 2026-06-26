from dataclasses import dataclass
from datetime import datetime

from search.domain.search_profile.value_objects import SearchProfileId
from search.domain.shared_kernel.value_objects import UserId


@dataclass(frozen=True, slots=True)
class KeywordDto:
    value: str


@dataclass(frozen=True, slots=True)
class SelectSearchProfileDto:
    id: str
    name: str


@dataclass(frozen=True, slots=True)
class SearchProfileDto:
    id: SearchProfileId
    user_id: UserId
    name: str
    keywords: list[KeywordDto]
    search_interval_minutes: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
