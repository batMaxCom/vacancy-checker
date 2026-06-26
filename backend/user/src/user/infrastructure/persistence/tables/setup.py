from user.infrastructure.persistence.tables.user import map_user_table


def setup_mapping() -> None:
    map_user_table()
