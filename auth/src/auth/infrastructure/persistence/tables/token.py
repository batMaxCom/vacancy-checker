from sqlalchemy import Column, DateTime, String, Table, Uuid
from sqlalchemy.orm import composite

from auth.domain.token.entity import RefreshToken
from auth.domain.token.value_objects import TokenHash
from auth.infrastructure.persistence.tables.base import MAPPER_REGISTRY

TOKEN_TABLE = Table(
    "refresh_tokens",
    MAPPER_REGISTRY.metadata,
    Column("token_id", Uuid, primary_key=True),
    Column("user_id", Uuid, nullable=False, index=True),
    Column("token_hash", String(64), nullable=False, unique=True),
    Column("device_id", String(255), nullable=True),
    Column("ip_address", String(45), nullable=False, server_default=""),
    Column("user_agent", String(512), nullable=False, server_default=""),
    Column("expires_at", DateTime(timezone=True), nullable=False),
    Column("revoked_at", DateTime(timezone=True), nullable=True),
    Column("replaced_by_token_id", Uuid, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
)


def map_token_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        RefreshToken,
        TOKEN_TABLE,
        properties={
            "_entity_id": TOKEN_TABLE.c.token_id,
            "_user_id": TOKEN_TABLE.c.user_id,
            "_token_hash_raw": TOKEN_TABLE.c.token_hash,
            "_device_id": TOKEN_TABLE.c.device_id,
            "_ip_address": TOKEN_TABLE.c.ip_address,
            "_user_agent": TOKEN_TABLE.c.user_agent,
            "_token_hash": composite(TokenHash, "_token_hash_raw"),
            "_expires_at": TOKEN_TABLE.c.expires_at,
            "_revoked_at": TOKEN_TABLE.c.revoked_at,
            "_replaced_by_token_id": TOKEN_TABLE.c.replaced_by_token_id,
            "_created_at": TOKEN_TABLE.c.created_at,
        },
    )
