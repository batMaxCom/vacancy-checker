from typing import Final, cast
from uuid import UUID

from starlette.requests import Request

from vacancy.application.common.application_error import ApplicationError, ApplicationTypeError
from vacancy.application.common.const.errors import INVALID_ROLE, MISSING_ROLE, MISSING_USER_ID
from vacancy.application.ports.auth import IdentityProvider
from vacancy.domain.shared_kernel.value_objects import UserId, UserRole


class IdentityProviderImpl(IdentityProvider):
    __USER_ID_HEADER: Final[str] = "X-User-ID"
    __API_ROLE_HEADER: Final[str] = "X-Api-Roles"

    def __init__(self, request: Request) -> None:
        self.__request = request

    def current_user_id(self) -> UserId:
        user_id = self.__request.headers.get(self.__USER_ID_HEADER)
        if not user_id:
            raise ApplicationError(
                type=ApplicationTypeError.UNAUTHORIZED,
                message=MISSING_USER_ID,
            )
        return UserId(UUID(user_id))

    def current_user_role(self) -> UserRole:
        role = self.__request.headers.get(self.__API_ROLE_HEADER)

        if not role:
            raise ApplicationError(
                type=ApplicationTypeError.UNAUTHORIZED,
                message=MISSING_ROLE,
            )
        user_role = cast(UserRole | None, getattr(UserRole, role, None))
        if user_role is not None:
            return user_role
        raise ApplicationError(
            type=ApplicationTypeError.UNAUTHORIZED,
            message=INVALID_ROLE,
        )
