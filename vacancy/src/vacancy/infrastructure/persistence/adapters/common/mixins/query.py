from collections.abc import Sequence

from sqlalchemy import Select, Table, select

from vacancy.domain.ports import Entity


class QueryMixin:
    @staticmethod
    def _get_query(
        entity: Table | type[Entity], fields: Sequence[str] | None = None
    ) -> Select:
        if isinstance(entity, Table):
            cols = [getattr(entity.c, field) for field in fields] if fields else [entity]
            return select(*cols)
        return select(entity)
