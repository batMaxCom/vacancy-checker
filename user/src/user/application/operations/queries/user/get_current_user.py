from dataclasses import dataclass

from sqlalchemy.exc import NoResultFound

from user.application.common.dto import UserDTO
from user.application.ports.cqrs import Query, QueryHandler
from user.domain.user.repository import UserRepository
from user.domain.user.value_objects import UserId


@dataclass(frozen=True, slots=True)
class GetCurrentUserQuery(Query[UserDTO | None]):
    user_id: UserId


class GetCurrentUserQueryHandler(QueryHandler[GetCurrentUserQuery, UserDTO | None]):
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.__user_repository = user_repository

    async def handle(self, query: GetCurrentUserQuery) -> UserDTO | None:
        try:
            user = await self.__user_repository.get(id=query.user_id)
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
