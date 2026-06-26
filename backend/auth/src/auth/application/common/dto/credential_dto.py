from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class UserCredentialDTO:
    user_id: str
    email: str
    password_hash: str
    password_salt: str | None
    is_email_verified: bool
    failed_login_attempts: int
    locked_until: datetime | None
    created_at: datetime
    updated_at: datetime
