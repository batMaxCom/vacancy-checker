from auth.infrastructure.persistence.tables.credential import map_credential_table
from auth.infrastructure.persistence.tables.token import map_token_table


def setup_mapping() -> None:
    map_credential_table()
    map_token_table()
