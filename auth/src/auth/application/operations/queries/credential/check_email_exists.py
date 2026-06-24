from dataclasses import dataclass

from auth.application.ports.cqrs import Query, QueryHandler
from auth.domain.credential.repository import CredentialRepository
from auth.domain.credential.value_objects import Email


@dataclass(frozen=True, slots=True)
class CheckEmailExistsQuery(Query[bool]):
    email: Email


class CheckEmailExistsQueryHandler(QueryHandler[CheckEmailExistsQuery, bool]):
    def __init__(
        self,
        credential_repository: CredentialRepository,
    ) -> None:
        self.__credential_repository = credential_repository

    async def handle(self, query: CheckEmailExistsQuery) -> bool:
        return await self.__credential_repository.exists(email=query.email)
