from datetime import datetime, timezone

from auth.domain.common.value_objects import UserId
from auth.domain.ports import Entity
from auth.domain.token.value_objects import TokenHash, TokenId


class RefreshToken(Entity[TokenId]):
    def __init__(
        self,
        token_id: TokenId,
        user_id: UserId,
        token_hash: TokenHash,
        expires_at: datetime,
        device_id: str | None = None,
        ip_address: str = "",
        user_agent: str = "",
        revoked_at: datetime | None = None,
        replaced_by_token_id: TokenId | None = None,
        created_at: datetime | None = None,
    ) -> None:
        super().__init__(token_id)
        self._user_id = user_id
        self._token_hash = token_hash
        self._device_id = device_id
        self._ip_address = ip_address
        self._user_agent = user_agent
        self._expires_at = expires_at
        self._revoked_at = revoked_at
        self._replaced_by_token_id = replaced_by_token_id
        self._created_at = created_at or datetime.now(timezone.utc)

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def token_hash(self) -> TokenHash:
        return self._token_hash

    @property
    def device_id(self) -> str | None:
        return self._device_id

    @property
    def ip_address(self) -> str:
        return self._ip_address

    @property
    def user_agent(self) -> str:
        return self._user_agent

    @property
    def expires_at(self) -> datetime:
        return self._expires_at

    @property
    def revoked_at(self) -> datetime | None:
        return self._revoked_at

    @property
    def replaced_by_token_id(self) -> TokenId | None:
        return self._replaced_by_token_id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self._expires_at

    @property
    def is_revoked(self) -> bool:
        return self._revoked_at is not None

    @property
    def is_valid(self) -> bool:
        return not self.is_expired and not self.is_revoked

    def revoke(self) -> None:
        self._revoked_at = datetime.now(timezone.utc)

    def replace(self, new_token_id: TokenId) -> None:
        self._revoked_at = datetime.now(timezone.utc)
        self._replaced_by_token_id = new_token_id
