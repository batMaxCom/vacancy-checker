from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table, Uuid
from sqlalchemy.orm import composite

from search.domain.search_profile.entity import SearchProfile
from search.domain.search_profile.value_objects import SearchInterval
from search.infrastructure.persistence.tables.base import MAPPER_REGISTRY
from search.infrastructure.persistence.tables.types import KeywordsColumn

SEARCH_PROFILE_TABLE = Table(
    "search_profiles",
    MAPPER_REGISTRY.metadata,
    Column("id", Uuid, primary_key=True),
    Column("user_id", Uuid, nullable=False),
    Column("name", String(255), nullable=False),
    Column("keywords", KeywordsColumn, nullable=False, default=list),
    Column("search_interval_minutes", Integer, nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)


def map_search_profile_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        SearchProfile,
        SEARCH_PROFILE_TABLE,
        properties={
            "_entity_id": SEARCH_PROFILE_TABLE.c.id,
            "_user_id": SEARCH_PROFILE_TABLE.c.user_id,
            "_name": SEARCH_PROFILE_TABLE.c.name,
            "_keywords": SEARCH_PROFILE_TABLE.c.keywords,
            "_search_interval": composite(
                SearchInterval,
                SEARCH_PROFILE_TABLE.c.search_interval_minutes,
            ),
            "_is_active": SEARCH_PROFILE_TABLE.c.is_active,
            "_created_at": SEARCH_PROFILE_TABLE.c.created_at,
            "_updated_at": SEARCH_PROFILE_TABLE.c.updated_at,
        },
    )
