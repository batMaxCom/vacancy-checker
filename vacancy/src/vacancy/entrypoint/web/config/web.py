from dataclasses import dataclass
from functools import lru_cache

from vacancy.entrypoint.web.config.app import AppConfig
from vacancy.entrypoint.web.config.db import PostgresConfig


@dataclass(frozen=True)
class WebConfig:
    app_config: AppConfig
    db_config: PostgresConfig


@lru_cache
def get_web_config() -> WebConfig:
    return WebConfig(
        app_config=AppConfig.from_env(),
        db_config=PostgresConfig.from_env()
    )
