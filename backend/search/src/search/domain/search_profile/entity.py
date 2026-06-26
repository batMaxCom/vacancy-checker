from datetime import datetime, timezone

from search.domain.ports import Entity
from search.domain.search_profile.value_objects import (
    Keyword,
    SearchInterval,
    SearchProfileId,
)
from search.domain.shared_kernel.value_objects import UserId


class SearchProfile(Entity[SearchProfileId]):
    def __init__(
        self,
        search_profile_id: SearchProfileId,
        user_id: UserId,
        name: str,
        keywords: list[Keyword],
        search_interval: SearchInterval,
        created_at: datetime,
        updated_at: datetime,
        is_active: bool = True,
    ) -> None:
        super().__init__(search_profile_id)
        self._user_id = user_id
        self._name = name
        self._keywords = keywords
        self._search_interval = search_interval
        self._created_at = created_at
        self._updated_at = updated_at
        self._is_active = is_active

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def keywords(self) -> list[Keyword]:
        return self._keywords

    @property
    def search_interval(self) -> SearchInterval:
        return self._search_interval

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def is_active(self) -> bool:
        return self._is_active

    def activate(self) -> None:
        self._is_active = True
        self._updated_at = datetime.now(tz=timezone.utc)

    def deactivate(self) -> None:
        self._is_active = False
        self._updated_at = datetime.now(tz=timezone.utc)

    def update_profile(
        self,
        name: str,
        keywords: list[Keyword],
        search_interval: SearchInterval,
    ) -> None:
        self._name = name
        self._keywords = keywords
        self._search_interval = search_interval
        self._updated_at = datetime.now(tz=timezone.utc)

    def add_keyword(self, keyword: Keyword) -> None:
        if keyword not in self._keywords:
            self._keywords = [*self._keywords, keyword]
            self._updated_at = datetime.now(tz=timezone.utc)

    def remove_keyword(self, keyword: str) -> None:
        self._keywords = [k for k in self._keywords if k.value != keyword]
        self._updated_at = datetime.now(tz=timezone.utc)

    def keyword_values(self) -> list[str]:
        return [k.value for k in self._keywords]
