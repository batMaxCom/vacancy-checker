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
        host = environ.get("RABBIT_HOST", "localhost")
        port = int(environ.get("RABBIT_PORT", "5672"))
        user = environ.get("RABBIT_USER", "user")
        password = environ.get("RABBIT_PASSWORD", "user_pwd")
        uri = f"amqp://{user}:{password}@{host}:{port}/"

        exchange_name = environ.get("RABBIT_EXCHANGE_NAME", "user")
        queue_name = environ.get("RABBIT_QUEUE_NAME", "user.queue")
        raw_keys = environ.get("RABBIT_ROUTING_KEYS", "user.#")
        routing_keys = tuple(k.strip() for k in raw_keys.split(","))

        return cls(
            host=host,
            port=port,
            user=user,
            password=password,
            uri=uri,
            exchange_name=exchange_name,
            queue_name=queue_name,
            routing_keys=routing_keys,
            reconnect_attempts=int(environ.get("RABBIT_RECONNECT_ATTEMPTS", "10")),
            reconnect_initial_delay_seconds=int(
                environ.get("RABBIT_RECONNECT_INITIAL_DELAY_SECONDS", "1")
            ),
            reconnect_max_delay_seconds=int(
                environ.get("RABBIT_RECONNECT_MAX_DELAY_SECONDS", "60")
            ),
        )
