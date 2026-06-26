from vacancy.infrastructure.persistence.tables.source import map_source_table
from vacancy.infrastructure.persistence.tables.vacancy import map_vacancy_table


def setup_mapping() -> None:
    map_source_table()
    map_vacancy_table()
