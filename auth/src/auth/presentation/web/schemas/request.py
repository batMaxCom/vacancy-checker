from dataclasses import dataclass


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str


@dataclass(frozen=True)
class RegisterRequest:
    email: str
    password: str
    first_name: str
    last_name: str


@dataclass(frozen=True)
class RefreshTokenRequest:
    refresh_token: str


@dataclass(frozen=True)
class LogoutRequest:
    refresh_token: str
