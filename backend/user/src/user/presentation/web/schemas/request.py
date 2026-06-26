from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserRequest:
    email: str
    first_name: str
    last_name: str


@dataclass(frozen=True)
class UpdateProfileRequest:
    first_name: str
    last_name: str
    avatar_url: str | None = None


@dataclass(frozen=True)
class ChangeRoleRequest:
    role: str
