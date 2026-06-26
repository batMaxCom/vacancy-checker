from datetime import datetime, timezone, timedelta

from auth.domain.common.value_objects import UserId
from auth.domain.credential.value_objects import Email, PasswordHash, PasswordSalt
from auth.domain.ports import Entity


class UserCredential(Entity[UserId]):
    def __init__(
        self,
        user_id: UserId,
        email: Email,
        password_hash: PasswordHash,
        password_salt: PasswordSalt | None = None,
        is_email_verified: bool = False,
        failed_login_attempts: int = 0,
        locked_until: datetime | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        super().__init__(user_id)
        self._email = email
        self._password_hash = password_hash
        self._password_salt = password_salt
        self._is_email_verified = is_email_verified
        self._failed_login_attempts = failed_login_attempts
        self._locked_until = locked_until
        now = datetime.now(timezone.utc)
        self._created_at = created_at or now
        self._updated_at = updated_at or now

    @property
    def email(self) -> Email:
        return self._email

    @property
    def password_hash(self) -> PasswordHash:
        return self._password_hash

    @property
    def password_salt(self) -> PasswordSalt | None:
        return self._password_salt

    @property
    def is_email_verified(self) -> bool:
        return self._is_email_verified

    @property
    def failed_login_attempts(self) -> int:
        return self._failed_login_attempts

    @property
    def locked_until(self) -> datetime | None:
        return self._locked_until

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def is_locked(self) -> bool:
        if self._locked_until is None:
            return False
        return datetime.now(timezone.utc) < self._locked_until

    def change_password(
        self,
        password_hash: PasswordHash,
        password_salt: PasswordSalt | None = None,
    ) -> None:
        self._password_hash = password_hash
        self._password_salt = password_salt
        self._updated_at = datetime.now(timezone.utc)

    def increment_failed_attempts(
        self,
        max_attempts: int = 5,
        lock_duration_minutes: int = 15,
    ) -> None:
        self._failed_login_attempts += 1
        if self._failed_login_attempts >= max_attempts:
            self._locked_until = datetime.now(timezone.utc) + timedelta(minutes=lock_duration_minutes)
        self._updated_at = datetime.now(timezone.utc)

    def reset_failed_attempts(self) -> None:
        self._failed_login_attempts = 0
        self._locked_until = None
        self._updated_at = datetime.now(timezone.utc)

    def lock(self, until: datetime) -> None:
        self._locked_until = until
        self._updated_at = datetime.now(timezone.utc)

    def unlock(self) -> None:
        self._locked_until = None
        self._updated_at = datetime.now(timezone.utc)

    def verify_email(self) -> None:
        self._is_email_verified = True
        self._updated_at = datetime.now(timezone.utc)
