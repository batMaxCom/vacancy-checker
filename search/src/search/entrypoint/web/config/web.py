from dataclasses import dataclass
from functools import lru_cache

from search.entrypoint.web.config import KafkaConfig
from search.entrypoint.web.config.app import AppConfig
from search.entrypoint.web.config.db import PostgresConfig
from search.entrypoint.web.config.tg import TgConfig


@dataclass(frozen=True)
class WebConfig:
    app_config: AppConfig
    db_config: PostgresConfig
    broker_config: KafkaConfig
    tg_config: TgConfig


@lru_cache
def get_web_config() -> WebConfig:
    return WebConfig(
        app_config=AppConfig.from_env(),
        db_config=PostgresConfig.from_env(),
        broker_config=KafkaConfig.from_env(),
        tg_config=TgConfig.from_env(),
    )
