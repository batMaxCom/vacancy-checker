from dataclasses import dataclass
from functools import lru_cache

from vacancy.entrypoint.web.config import AuthConfig, KafkaConfig
from vacancy.entrypoint.web.config.app import AppConfig
from vacancy.entrypoint.web.config.db import PostgresConfig


@dataclass(frozen=True)
class WebConfig:
    app_config: AppConfig
    auth_config: AuthConfig
    db_config: PostgresConfig
    broker_config: KafkaConfig


@lru_cache
def get_web_config() -> WebConfig:
    return WebConfig(
        app_config=AppConfig.from_env(),
        auth_config=AuthConfig.from_env(),
        db_config=PostgresConfig.from_env(),
        broker_config=KafkaConfig.from_env()
    )
