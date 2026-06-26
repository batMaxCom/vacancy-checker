from vacancy.application.ports.auth import PermissionChecker
from vacancy.domain.shared_kernel.value_objects import UserRole


class PermissionCheckerImpl(PermissionChecker):
    """Реализация проверки ролей у пользователя."""

    def is_user(self, role: UserRole) -> bool:
        return role is UserRole.USER

    def is_employee(self, role: UserRole) -> bool:
        return role is UserRole.EMPLOYER

    def is_admin(self, role: UserRole) -> bool:
        return role is UserRole.ADMIN

    def is_authorize(self, role: UserRole) -> bool:
        return role in UserRole
