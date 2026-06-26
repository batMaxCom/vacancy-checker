from sqlalchemy import Column, DateTime, String, Table, Uuid
from sqlalchemy.orm import composite

from user.domain.user.entity import User
from user.domain.user.value_objects import (
    AvatarUrl,
    Email,
    FirstName,
    LastName,
    UserRole,
    UserStatus,
)
from user.infrastructure.persistence.tables.base import MAPPER_REGISTRY
from user.infrastructure.persistence.tables.types import EnumAsString

USER_TABLE = Table(
    "user",
    MAPPER_REGISTRY.metadata,
    Column("id", Uuid, primary_key=True),
    Column("email", String(255), nullable=False, unique=True),
    Column("first_name", String(100), nullable=False),
    Column("last_name", String(100), nullable=False),
    Column("avatar_url", String(500), nullable=True),
    Column("role", EnumAsString(UserRole, length=20), nullable=False),
    Column("status", EnumAsString(UserStatus, length=20), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)


def map_user_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        User,
        USER_TABLE,
        properties={
            "_entity_id": USER_TABLE.c.id,
            "_email_raw": USER_TABLE.c.email,
            "_first_name_raw": USER_TABLE.c.first_name,
            "_last_name_raw": USER_TABLE.c.last_name,
            "_avatar_url_raw": USER_TABLE.c.avatar_url,
            "_email": composite(Email, "_email_raw"),
            "_first_name": composite(FirstName, "_first_name_raw"),
            "_last_name": composite(LastName, "_last_name_raw"),
            "_avatar_url": composite(AvatarUrl, "_avatar_url_raw"),
            "_role": USER_TABLE.c.role,
            "_status": USER_TABLE.c.status,
            "_created_at": USER_TABLE.c.created_at,
            "_updated_at": USER_TABLE.c.updated_at,
        },
    )
