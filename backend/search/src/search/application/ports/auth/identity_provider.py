from abc import ABC, abstractmethod

from search.domain.shared_kernel.value_objects import UserId, UserRole


class IdentityProvider(ABC):
    @abstractmethod
    def current_user_id(self) -> UserId: ...

    @abstractmethod
    def current_user_role(self) -> UserRole: ...
