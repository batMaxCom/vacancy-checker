from dataclasses import dataclass
from os import environ
from typing import Self

@dataclass(frozen=True)
class RabbitMQConfig:
    """Класс конфигурации для RabbitMQ."""

    host: str
    port: int
    user: str
    password: str
    uri: str

    exchange_name: str

    @classmethod
    def from_env(cls) -> Self:
        """Возвращает настройки RabbitMQ."""
        host = environ.get("RABBITMQ_HOST", "localhost")
        port = int(environ.get("RABBITMQ_PORT", "5432"))
        user = environ.get("RABBITMQ_USER", "user")
        password = environ.get("RABBITMQ_PASS", "user_pwd")
        uri = f"amqp://{user}:{password}@{host}:{port}/"

        exchange_name = environ.get(
            "RABBITMQ_EXCHANGE_NAME", "exchange_name"
        )

        return cls(
            host=host,
            port=port,
            user=user,
            password=password,
            uri=uri,
            exchange_name=exchange_name,
        )
