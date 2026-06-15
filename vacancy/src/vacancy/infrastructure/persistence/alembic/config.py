from functools import lru_cache
from importlib.resources import files

from alembic.config import Config as AlembicConfig

from vacancy.entrypoint.web.config.web import get_web_config


@lru_cache
def get_alembic_config() -> AlembicConfig:
    resource = files("vacancy.infrastructure.persistence.alembic")
    alembic_config = resource.joinpath("alembic.ini")
    config_object = AlembicConfig(str(alembic_config))
    config_object.set_main_option(
        "sqlalchemy.url", get_web_config().db_config.asyncpg_uri
    )
    return config_object
