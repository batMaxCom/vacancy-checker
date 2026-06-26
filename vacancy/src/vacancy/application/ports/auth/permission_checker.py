from abc import ABC, abstractmethod

from vacancy.domain.shared_kernel.value_objects import UserRole


class PermissionChecker(ABC):

    @abstractmethod
    def is_user(self, role: UserRole) -> bool: ...

    @abstractmethod
    def is_employee(self, role: UserRole) -> bool: ...

    @abstractmethod
    def is_admin(self, role: UserRole) -> bool: ...

    @abstractmethod
    def is_authorize(self, role: UserRole) -> bool: ...
