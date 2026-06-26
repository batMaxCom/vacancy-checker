from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table, Uuid
from sqlalchemy.orm import composite

from auth.domain.credential.entity import UserCredential
from auth.domain.credential.value_objects import Email, PasswordHash, PasswordSalt
from auth.infrastructure.persistence.tables.base import MAPPER_REGISTRY

CREDENTIAL_TABLE = Table(
    "user_credentials",
    MAPPER_REGISTRY.metadata,
    Column("user_id", Uuid, primary_key=True),
    Column("email", String(255), nullable=False, unique=True),
    Column("password_hash", String(512), nullable=False),
    Column("password_salt", String(256), nullable=True),
    Column("is_email_verified", Boolean, nullable=False, default=False),
    Column("failed_login_attempts", Integer, nullable=False, default=0),
    Column("locked_until", DateTime(timezone=True), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)


def map_credential_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        UserCredential,
        CREDENTIAL_TABLE,
        properties={
            "_entity_id": CREDENTIAL_TABLE.c.user_id,
            "_email_raw": CREDENTIAL_TABLE.c.email,
            "_password_hash_raw": CREDENTIAL_TABLE.c.password_hash,
            "_password_salt_raw": CREDENTIAL_TABLE.c.password_salt,
            "_email": composite(Email, "_email_raw"),
            "_password_hash": composite(PasswordHash, "_password_hash_raw"),
            "_password_salt": composite(PasswordSalt, "_password_salt_raw"),
            "_is_email_verified": CREDENTIAL_TABLE.c.is_email_verified,
            "_failed_login_attempts": CREDENTIAL_TABLE.c.failed_login_attempts,
            "_locked_until": CREDENTIAL_TABLE.c.locked_until,
            "_created_at": CREDENTIAL_TABLE.c.created_at,
            "_updated_at": CREDENTIAL_TABLE.c.updated_at,
        },
    )
