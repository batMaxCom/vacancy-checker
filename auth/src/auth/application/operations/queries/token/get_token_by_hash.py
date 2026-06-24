from dataclasses import dataclass

from sqlalchemy.exc import NoResultFound

from auth.application.common.dto.token_dto import RefreshTokenDTO
from auth.application.ports.cqrs import Query, QueryHandler
from auth.domain.token.repository import TokenRepository
from auth.domain.token.value_objects import TokenHash


@dataclass(frozen=True, slots=True)
class GetRefreshTokenByHashQuery(Query[RefreshTokenDTO | None]):
    token_hash: TokenHash


class GetRefreshTokenByHashQueryHandler(
    QueryHandler[GetRefreshTokenByHashQuery, RefreshTokenDTO | None],
):
    def __init__(
        self,
        token_repository: TokenRepository,
    ) -> None:
        self.__token_repository = token_repository

    async def handle(self, query: GetRefreshTokenByHashQuery) -> RefreshTokenDTO | None:
        try:
            token = await self.__token_repository.get(token_hash=query.token_hash)
        except NoResultFound:
            return None

        return RefreshTokenDTO(
            token_id=str(token.entity_id),
            user_id=str(token.user_id),
            token_hash=token.token_hash.value,
            device_id=token.device_id,
            ip_address=token.ip_address,
            user_agent=token.user_agent,
            expires_at=token.expires_at,
            revoked_at=token.revoked_at,
            replaced_by_token_id=str(token.replaced_by_token_id) if token.replaced_by_token_id else None,
            created_at=token.created_at,
        )
