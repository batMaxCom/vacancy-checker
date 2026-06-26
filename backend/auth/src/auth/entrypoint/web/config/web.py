from dataclasses import dataclass
from functools import lru_cache

from auth.entrypoint.web.config.app import AppConfig
from auth.entrypoint.web.config.auth import AuthConfig
from auth.entrypoint.web.config.broker import RabbitMQConfig
from auth.entrypoint.web.config.db import PostgresConfig


@dataclass(frozen=True)
class WebConfig:
    app_config: AppConfig
    db_config: PostgresConfig
    auth_settings: AuthConfig
    broker_config: RabbitMQConfig


@lru_cache
def get_web_config() -> WebConfig:
    return WebConfig(
        app_config=AppConfig.from_env(),
        db_config=PostgresConfig.from_env(),
        auth_settings=AuthConfig.from_env(),
        broker_config=RabbitMQConfig.from_env(),
    )
