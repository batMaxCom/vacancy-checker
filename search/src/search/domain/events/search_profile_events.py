from dataclasses import dataclass
from datetime import datetime, timezone

from search.domain.common.value_objects import UserId
from search.domain.events.base_event import DomainEvent
from search.domain.search_profile.value_objects import SearchProfileId


@dataclass(frozen=True, slots=True)
class SearchProfileActivated(DomainEvent):
    profile_id: SearchProfileId
    user_id: UserId


@dataclass(frozen=True, slots=True)
class SearchProfileDeactivated(DomainEvent):
    profile_id: SearchProfileId
    user_id: UserId


def search_profile_activated(
    profile_id: SearchProfileId,
    user_id: UserId,
    occurred_at: datetime | None = None,
) -> SearchProfileActivated:
    return SearchProfileActivated(
        profile_id=profile_id,
        user_id=user_id,
        occurred_at=occurred_at or datetime.now(tz=timezone.utc),
    )


def search_profile_deactivated(
    profile_id: SearchProfileId,
    user_id: UserId,
    occurred_at: datetime | None = None,
) -> SearchProfileDeactivated:
    return SearchProfileDeactivated(
        profile_id=profile_id,
        user_id=user_id,
        occurred_at=occurred_at or datetime.now(tz=timezone.utc),
    )
