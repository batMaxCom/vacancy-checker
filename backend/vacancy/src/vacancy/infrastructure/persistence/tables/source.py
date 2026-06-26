from sqlalchemy import Boolean, Column, String, Table, Uuid

from vacancy.domain.sources.entity import Source
from vacancy.infrastructure.persistence.tables.base import MAPPER_REGISTRY

SOURCE_TABLE = Table(
    "source",
    MAPPER_REGISTRY.metadata,
    Column("id", Uuid, primary_key=True),
    Column("name", String(255), nullable=False, unique=True),
    Column("base_url", String(500), nullable=False, default=""),
    Column("is_active", Boolean, nullable=False, default=True),
)


def map_source_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        Source,
        SOURCE_TABLE,
        properties={
            "_entity_id": SOURCE_TABLE.c.id,
            "_name": SOURCE_TABLE.c.name,
            "_base_url": SOURCE_TABLE.c.base_url,
            "_is_active": SOURCE_TABLE.c.is_active,
        },
    )
