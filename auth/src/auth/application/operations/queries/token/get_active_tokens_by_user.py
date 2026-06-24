from dataclasses import dataclass

from auth.application.common.dto.token_dto import RefreshTokenDTO
from auth.application.ports.cqrs import Query, QueryHandler
from auth.domain.common.value_objects import UserId
from auth.domain.token.repository import TokenRepository


@dataclass(frozen=True, slots=True)
class GetActiveTokensByUserQuery(Query[list[RefreshTokenDTO]]):
    user_id: UserId


class GetActiveTokensByUserQueryHandler(
    QueryHandler[GetActiveTokensByUserQuery, list[RefreshTokenDTO]],
):
    def __init__(
        self,
        token_repository: TokenRepository,
    ) -> None:
        self.__token_repository = token_repository

    async def handle(self, query: GetActiveTokensByUserQuery) -> list[RefreshTokenDTO]:
        tokens = await self.__token_repository.get_all(
            user_id=query.user_id,
        )

        result: list[RefreshTokenDTO] = []
        for token in tokens:
            if token.is_valid:
                result.append(
                    RefreshTokenDTO(
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
                    ),
                )

        return result
