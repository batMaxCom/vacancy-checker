from dataclasses import dataclass
from functools import lru_cache

from user.entrypoint.web.config.app import AppConfig
from user.entrypoint.web.config.auth import AuthConfig
from user.entrypoint.web.config.broker import RabbitMQConfig
from user.entrypoint.web.config.db import PostgresConfig


@dataclass(frozen=True)
class WebConfig:
    app_config: AppConfig
    auth_config: AuthConfig
    db_config: PostgresConfig
    broker_config: RabbitMQConfig


@lru_cache
def get_web_config() -> WebConfig:
    return WebConfig(
        app_config=AppConfig.from_env(),
        auth_config=AuthConfig.from_env(),
        db_config=PostgresConfig.from_env(),
        broker_config=RabbitMQConfig.from_env(),
    )
