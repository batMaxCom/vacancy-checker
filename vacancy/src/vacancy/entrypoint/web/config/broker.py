from dataclasses import dataclass
from os import environ
from typing import Self


@dataclass(frozen=True)
class KafkaConfig:
    """Конфигурация Kafka Consumer."""

    bootstrap_servers: str
    client_id: str

    # consumer group
    group_id: str

    # offset handling
    auto_offset_reset: str
    enable_auto_commit: bool

    # consumer liveness
    session_timeout_ms: int
    heartbeat_interval_ms: int

    # network
    request_timeout_ms: int
    socket_timeout_ms: int

    # polling
    poll_timeout_seconds: float

    # reconnect
    reconnect_attempts: int
    reconnect_initial_delay_seconds: int
    reconnect_max_delay_seconds: int

    @classmethod
    def from_env(cls) -> Self:
        """Создать конфигурацию из переменных окружения."""
        return cls(
            bootstrap_servers=environ.get(
                "KAFKA_BOOTSTRAP_SERVERS",
                "localhost:9092",
            ),
            client_id=environ.get(
                "KAFKA_CLIENT_ID",
                "app",
            ),

            group_id=environ.get(
                "KAFKA_GROUP_ID",
                "app-consumer-group",
            ),

            auto_offset_reset=environ.get(
                "KAFKA_AUTO_OFFSET_RESET",
                "earliest",
            ),

            enable_auto_commit=environ.get(
                "KAFKA_ENABLE_AUTO_COMMIT",
                "false",
            ).lower() == "true",

            session_timeout_ms=int(
                environ.get(
                    "KAFKA_SESSION_TIMEOUT_MS",
                    "45000",
                )
            ),

            heartbeat_interval_ms=int(
                environ.get(
                    "KAFKA_HEARTBEAT_INTERVAL_MS",
                    "15000",
                )
            ),

            request_timeout_ms=int(
                environ.get(
                    "KAFKA_REQUEST_TIMEOUT_MS",
                    "30000",
                )
            ),

            socket_timeout_ms=int(
                environ.get(
                    "KAFKA_SOCKET_TIMEOUT_MS",
                    "30000",
                )
            ),

            poll_timeout_seconds=float(
                environ.get(
                    "KAFKA_POLL_TIMEOUT_SECONDS",
                    "1",
                )
            ),

            reconnect_attempts=int(
                environ.get(
                    "KAFKA_RECONNECT_ATTEMPTS",
                    "10",
                )
            ),

            reconnect_initial_delay_seconds=int(
                environ.get(
                    "KAFKA_RECONNECT_INITIAL_DELAY_SECONDS",
                    "1",
                )
            ),

            reconnect_max_delay_seconds=int(
                environ.get(
                    "KAFKA_RECONNECT_MAX_DELAY_SECONDS",
                    "60",
                )
            ),
        )

    def to_dict(self) -> dict:
        """Конфигурация для confluent_kafka.Consumer."""
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "client.id": self.client_id,

            # consumer group
            "group.id": self.group_id,

            # offset management
            "auto.offset.reset": self.auto_offset_reset,
            "enable.auto.commit": self.enable_auto_commit,

            # liveness
            "session.timeout.ms": self.session_timeout_ms,
            "heartbeat.interval.ms": self.heartbeat_interval_ms,

            # network
            "request.timeout.ms": self.request_timeout_ms,
            "socket.timeout.ms": self.socket_timeout_ms,
        }
