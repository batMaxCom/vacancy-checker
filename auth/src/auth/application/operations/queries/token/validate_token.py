from dataclasses import dataclass

from sqlalchemy.exc import NoResultFound

from auth.application.ports.cqrs import Query, QueryHandler
from auth.domain.token.repository import TokenRepository
from auth.domain.token.value_objects import TokenHash


@dataclass(frozen=True, slots=True)
class ValidateRefreshTokenQuery(Query[bool]):
    token_hash: TokenHash


class ValidateRefreshTokenQueryHandler(
    QueryHandler[ValidateRefreshTokenQuery, bool],
):
    def __init__(
        self,
        token_repository: TokenRepository,
    ) -> None:
        self.__token_repository = token_repository

    async def handle(self, query: ValidateRefreshTokenQuery) -> bool:
        try:
            token = await self.__token_repository.get(token_hash=query.token_hash)
        except NoResultFound:
            return False

        return token.is_valid
