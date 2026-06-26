from user.application.ports.auth import PermissionChecker
from user.domain.user import UserRole


class PermissionCheckerImpl(PermissionChecker):
    """Реализация проверки ролей у пользователя."""

    def is_user(self, role: UserRole) -> bool:
        return role.name == UserRole.USER


    def is_employee(self, role: UserRole) -> bool:
        return role.name == UserRole.EMPLOYER


    def is_admin(self, role: UserRole) -> bool:
        return role.name == UserRole.ADMIN


    def is_authorize(self, role: UserRole) -> bool:
        return role.name in (role_name for role_name in UserRole)
