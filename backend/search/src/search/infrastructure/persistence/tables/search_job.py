from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, Uuid

from search.domain.search_job.entity import SearchJob
from search.infrastructure.persistence.tables.base import MAPPER_REGISTRY
from search.infrastructure.persistence.tables.types import SearchJobStatusColumn

SEARCH_JOB_TABLE = Table(
    "search_jobs",
    MAPPER_REGISTRY.metadata,
    Column("id", Uuid, primary_key=True),
    Column("profile_id", Uuid, ForeignKey("search_profiles.id"), nullable=False),
    Column("started_at", DateTime(timezone=True), nullable=False),
    Column("finished_at", DateTime(timezone=True), nullable=True),
    Column("status", SearchJobStatusColumn(50), nullable=False),
    Column("vacancies_found", Integer, default=0),
)


def map_search_job_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        SearchJob,
        SEARCH_JOB_TABLE,
        properties={
            "_entity_id": SEARCH_JOB_TABLE.c.id,
            "_profile_id": SEARCH_JOB_TABLE.c.profile_id,
            "_started_at": SEARCH_JOB_TABLE.c.started_at,
            "_finished_at": SEARCH_JOB_TABLE.c.finished_at,
            "_status": SEARCH_JOB_TABLE.c.status,
            "_vacancies_found": SEARCH_JOB_TABLE.c.vacancies_found,
        },
    )
