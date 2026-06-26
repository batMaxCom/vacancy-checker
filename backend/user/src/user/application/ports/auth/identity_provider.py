from abc import ABC, abstractmethod

from user.domain.user import UserId, UserRole


class IdentityProvider(ABC):
    @abstractmethod
    def current_user_id(self) -> UserId: ...

    @abstractmethod
    def current_user_role(self) -> UserRole: ...
