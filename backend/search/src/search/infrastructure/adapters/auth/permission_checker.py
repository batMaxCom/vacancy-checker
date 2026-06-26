from search.application.ports.auth import PermissionChecker
from search.domain.shared_kernel.value_objects import UserRole


class PermissionCheckerImpl(PermissionChecker):
    """Реализация проверки ролей у пользователя."""

    def is_user(self, role: UserRole) -> bool:
        return role == UserRole.USER


    def is_employee(self, role: UserRole) -> bool:
        return role == UserRole.EMPLOYER


    def is_admin(self, role: UserRole) -> bool:
        return role == UserRole.ADMIN


    def is_authorize(self, role: UserRole) -> bool:
        return role in UserRole
