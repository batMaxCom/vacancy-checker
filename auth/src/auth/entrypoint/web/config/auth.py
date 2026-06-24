from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class AuthConfig:
    secret_key: str = "changeme"
    access_token_expires_seconds: int = field(default=900)
    refresh_token_expires_seconds: int = field(default=2_592_000)
