from dataclasses import dataclass

from auth.application.common.dto.credential_dto import UserCredentialDTO
from auth.application.ports.cqrs import Query, QueryHandler
from auth.domain.credential.repository import CredentialRepository
from auth.domain.credential.value_objects import Email


@dataclass(frozen=True, slots=True)
class GetUserCredentialByEmailQuery(Query[UserCredentialDTO | None]):
    email: Email


class GetUserCredentialByEmailQueryHandler(
    QueryHandler[GetUserCredentialByEmailQuery, UserCredentialDTO | None],
):
    def __init__(
        self,
        credential_repository: CredentialRepository,
    ) -> None:
        self.__credential_repository = credential_repository

    async def handle(self, query: GetUserCredentialByEmailQuery) -> UserCredentialDTO | None:
        credential = await self.__credential_repository.get(email=query.email)

        if credential is None:
            return None

        return UserCredentialDTO(
            user_id=str(credential.entity_id),
            email=credential.email.value,
            password_hash=credential.password_hash.value,
            password_salt=credential.password_salt.value if credential.password_salt else None,
            is_email_verified=credential.is_email_verified,
            failed_login_attempts=credential.failed_login_attempts,
            locked_until=credential.locked_until,
            created_at=credential.created_at,
            updated_at=credential.updated_at,
        )
