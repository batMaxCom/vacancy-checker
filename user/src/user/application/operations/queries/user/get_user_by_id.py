from dataclasses import dataclass

from sqlalchemy.exc import NoResultFound

from user.application.common.dto import UserBriefDTO
from user.application.ports.cqrs import Query, QueryHandler
from user.domain.user.repository import UserRepository
from user.domain.user.value_objects import UserId


@dataclass(frozen=True, slots=True)
class GetUserByIdQuery(Query[UserBriefDTO | None]):
    user_id: UserId


class GetUserByIdQueryHandler(QueryHandler[GetUserByIdQuery, UserBriefDTO | None]):
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.__user_repository = user_repository

    async def handle(self, query: GetUserByIdQuery) -> UserBriefDTO | None:
        try:
            user = await self.__user_repository.get(id=query.user_id)
        except NoResultFound:
            return None

        return UserBriefDTO(
            id=str(user.entity_id),
            email=user.email.value,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
        )
