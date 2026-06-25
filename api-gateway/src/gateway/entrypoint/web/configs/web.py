from dataclasses import dataclass
from functools import lru_cache

from gateway.entrypoint.web.configs.app import GatewayConfig, AppConfig


@dataclass(frozen=True)
class WebConfig:
    app_config: AppConfig
    gateway_config: GatewayConfig


@lru_cache
def get_web_config() -> WebConfig:
    return WebConfig(
        app_config=AppConfig.from_env(),
        gateway_config=GatewayConfig.from_env(),
    )
