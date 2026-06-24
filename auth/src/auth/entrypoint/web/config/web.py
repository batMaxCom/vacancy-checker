from dataclasses import dataclass
from functools import lru_cache

from auth.entrypoint.web.config.app import AppConfig
from auth.entrypoint.web.config.db import PostgresConfig
from auth.entrypoint.web.config.auth import AuthConfig


@dataclass(frozen=True)
class WebConfig:
    app_config: AppConfig
    db_config: PostgresConfig
    auth_settings: AuthConfig


@lru_cache
def get_web_config() -> WebConfig:
    return WebConfig(
        app_config=AppConfig.from_env(),
        db_config=PostgresConfig.from_env(),
        auth_settings=AuthConfig(),
    )
