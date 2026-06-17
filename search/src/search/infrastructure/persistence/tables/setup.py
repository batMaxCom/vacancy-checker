from search.infrastructure.persistence.tables.search_job import map_search_job_table
from search.infrastructure.persistence.tables.search_profile import map_search_profile_table


def setup_mapping() -> None:
    map_search_job_table()
    map_search_profile_table()
