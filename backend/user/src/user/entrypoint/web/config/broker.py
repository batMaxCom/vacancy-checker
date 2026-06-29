from dataclasses import dataclass
from os import environ
from typing import Self


@dataclass(frozen=True)
class RabbitMQConfig:
    host: str
    port: int
    user: str
    password: str
    uri: str

    exchange_name: str
    queue_name: str
    routing_keys: tuple[str, ...]

    reconnect_attempts: int
    reconnect_initial_delay_seconds: int
    reconnect_max_delay_seconds: int

    @classmethod
    def from_env(cls) -> Self:
        host = environ.get("RABBITMQ_HOST", "localhost")
        port = int(environ.get("RABBITMQ_PORT", "5672"))
        user = environ.get("RABBITMQ_USER", "user")
        password = environ.get("RABBITMQ_PASS", "user_pwd")
        uri = f"amqp://{user}:{password}@{host}:{port}/"

        exchange_name = environ.get("RABBITMQ_EXCHANGE_NAME", "user")
        queue_name = environ.get("RABBITMQ_QUEUE_NAME", "user.queue")
        raw_keys = environ.get("RABBITMQ_ROUTING_KEYS", "user.#")
        routing_keys = tuple(k.strip() for k in raw_keys.split(","))

        reconnect_attempts = int(environ.get("RABBITMQ_RECONNECT_ATTEMPTS", "10"))
        reconnect_initial_delay_seconds = int(
                environ.get("RABBITMQ_RECONNECT_INITIAL_DELAY_SECONDS", "1")
            )
        reconnect_max_delay_seconds = int(
                environ.get("RABBITMQ_RECONNECT_MAX_DELAY_SECONDS", "60")
            )

        return cls(
            host=host,
            port=port,
            user=user,
            password=password,
            uri=uri,
            exchange_name=exchange_name,
            queue_name=queue_name,
            routing_keys=routing_keys,
            reconnect_attempts=reconnect_attempts,
            reconnect_initial_delay_seconds=reconnect_initial_delay_seconds,
            reconnect_max_delay_seconds=reconnect_max_delay_seconds,
        )
