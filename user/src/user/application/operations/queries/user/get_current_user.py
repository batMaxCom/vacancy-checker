from dataclasses import dataclass

from sqlalchemy.exc import NoResultFound

from user.application.common.dto import UserDTO
from user.application.ports.auth import IdentityProvider
from user.application.ports.cqrs import Query, QueryHandler
from user.domain.user.repository import UserRepository
from user.domain.user.value_objects import UserId


@dataclass(frozen=True, slots=True)
class GetCurrentUserQuery(Query[UserDTO | None]):
    ...

class GetCurrentUserQueryHandler(QueryHandler[GetCurrentUserQuery, UserDTO | None]):
    def __init__(
        self,
        user_repository: UserRepository,
        identity_provider: IdentityProvider
    ) -> None:
        self.__user_repository = user_repository
        self.__identity_provider = identity_provider

    async def handle(self, query: GetCurrentUserQuery) -> UserDTO | None:
        user_id = self.__identity_provider.current_user_id()
        try:
            user = await self.__user_repository.get(id=UserId(user_id))
        except NoResultFound:
            return None

        return UserDTO(
            id=str(user.entity_id),
            email=user.email.value,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            role=user.role.name,
            status=user.status.name,
        )
