from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, Table, Text, Uuid
from sqlalchemy.orm import composite

from vacancy.domain.vacancies.entity import Vacancy
from vacancy.domain.vacancies.value_objects import Salary
from vacancy.infrastructure.persistence.tables.base import MAPPER_REGISTRY

VACANCY_TABLE = Table(
    "vacancy",
    MAPPER_REGISTRY.metadata,
    Column("id", Uuid, primary_key=True),
    Column("source_id", Uuid, ForeignKey("source.id"), nullable=False),
    Column("external_id", String(255), nullable=True),
    Column("title", String(255), nullable=False),
    Column("description", Text, nullable=False),
    Column("company_name", String(255), nullable=True),
    Column("employment_type", String(50), nullable=False),
    Column("work_format", String(50), nullable=False),
    Column("salary_min_amount", Numeric(10, 2), nullable=True),
    Column("salary_max_amount", Numeric(10, 2), nullable=True),
    Column("location", String(255), nullable=True),
    Column("url", String(500), nullable=False),
    Column("published_at", DateTime(timezone=True), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    Column("status", String(50), nullable=False),
)


def map_vacancy_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        Vacancy,
        VACANCY_TABLE,
        properties={
            "_entity_id": VACANCY_TABLE.c.id,
            "_source_id": VACANCY_TABLE.c.source_id,
            "_external_id": VACANCY_TABLE.c.external_id,
            "_title": VACANCY_TABLE.c.title,
            "_description": VACANCY_TABLE.c.description,
            "_company_name": VACANCY_TABLE.c.company_name,
            "_employment_type": VACANCY_TABLE.c.employment_type,
            "_work_format": VACANCY_TABLE.c.work_format,
            "_salary": composite(
                Salary,
                VACANCY_TABLE.c.salary_min_amount,
                VACANCY_TABLE.c.salary_max_amount
            ),
            "_location": VACANCY_TABLE.c.location,
            "_url": VACANCY_TABLE.c.url,
            "_published_at": VACANCY_TABLE.c.published_at,
            "_created_at": VACANCY_TABLE.c.created_at,
            "_updated_at": VACANCY_TABLE.c.updated_at,
            "_status": VACANCY_TABLE.c.status,
        },
    )
