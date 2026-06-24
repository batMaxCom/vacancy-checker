from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthContext:
    user_id: str
    role: str
    is_valid: bool
    expires_at: int | None = None
