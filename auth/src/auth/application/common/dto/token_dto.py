from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class RefreshTokenDTO:
    token_id: str
    user_id: str
    token_hash: str
    device_id: str | None
    ip_address: str
    user_agent: str
    expires_at: datetime
    revoked_at: datetime | None
    replaced_by_token_id: str | None
    created_at: datetime
