from datetime import UTC, datetime

from user.domain.ports import Entity
from user.domain.user.value_objects import (
    AvatarUrl,
    Email,
    FirstName,
    LastName,
    UserId,
    UserRole,
    UserStatus,
)


class User(Entity[UserId]):
    def __init__(
        self,
        user_id: UserId,
        email: Email,
        first_name: FirstName,
        last_name: LastName,
        role: UserRole,
        status: UserStatus,
        avatar_url: AvatarUrl | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        super().__init__(user_id)
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._avatar_url = avatar_url
        self._role = role
        self._status = status
        now = datetime.now(UTC)
        self._created_at = created_at or now
        self._updated_at = updated_at or now

    @property
    def email(self) -> Email:
        return self._email

    @property
    def first_name(self) -> FirstName:
        return self._first_name

    @property
    def last_name(self) -> LastName:
        return self._last_name

    @property
    def avatar_url(self) -> AvatarUrl | None:
        return self._avatar_url

    @property
    def role(self) -> UserRole:
        return self._role

    @property
    def status(self) -> UserStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def update_profile(
        self,
        first_name: FirstName,
        last_name: LastName,
        avatar_url: AvatarUrl | None = None,
    ) -> None:
        self._first_name = first_name
        self._last_name = last_name
        self._avatar_url = avatar_url
        self._updated_at = datetime.now(UTC)

    def change_email(self, email: Email) -> None:
        self._email = email
        self._updated_at = datetime.now(UTC)

    def change_role(self, role: UserRole) -> None:
        self._role = role
        self._updated_at = datetime.now(UTC)

    def change_status(self, status: UserStatus) -> None:
        self._status = status
        self._updated_at = datetime.now(UTC)

    def deactivate(self) -> None:
        self._status = UserStatus.INACTIVE
        self._updated_at = datetime.now(UTC)

    def activate(self) -> None:
        self._status = UserStatus.ACTIVE
        self._updated_at = datetime.now(UTC)
