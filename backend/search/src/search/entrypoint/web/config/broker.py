from dataclasses import dataclass
from os import environ
from typing import Self


@dataclass(frozen=True)
class KafkaConfig:
    bootstrap_servers: str
    client_id: str

    # reliability
    acks: str
    enable_idempotence: bool

    # retry
    retries: int
    retry_backoff_ms: int
    delivery_timeout_ms: int

    # network
    request_timeout_ms: int
    socket_timeout_ms: int

    # batching / throughput
    linger_ms: int
    batch_size: int
    compression_type: str

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            bootstrap_servers=environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            client_id=environ.get("KAFKA_CLIENT_ID", "app"),

            acks=environ.get("KAFKA_ACKS", "all"),
            enable_idempotence=environ.get("KAFKA_ENABLE_IDEMPOTENCE", "true").lower() == "true",

            retries=int(environ.get("KAFKA_RETRIES", "10")),
            retry_backoff_ms=int(environ.get("KAFKA_RETRY_BACKOFF_MS", "1000")),
            delivery_timeout_ms=int(environ.get("KAFKA_DELIVERY_TIMEOUT_MS", "120000")),

            request_timeout_ms=int(environ.get("KAFKA_REQUEST_TIMEOUT_MS", "30000")),
            socket_timeout_ms=int(environ.get("KAFKA_SOCKET_TIMEOUT_MS", "30000")),

            linger_ms=int(environ.get("KAFKA_LINGER_MS", "5")),
            batch_size=int(environ.get("KAFKA_BATCH_SIZE", "16384")),
            compression_type=environ.get("KAFKA_COMPRESSION_TYPE", "snappy"),
        )

    def to_dict(self) -> dict:
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "client.id": self.client_id,

            # reliability
            "acks": self.acks,
            "enable.idempotence": self.enable_idempotence,

            # retry
            "retries": self.retries,
            "retry.backoff.ms": self.retry_backoff_ms,
            "delivery.timeout.ms": self.delivery_timeout_ms,

            # network
            "request.timeout.ms": self.request_timeout_ms,
            "socket.timeout.ms": self.socket_timeout_ms,

            # batching
            "linger.ms": self.linger_ms,
            "batch.size": self.batch_size,
            "compression.type": self.compression_type,
        }
