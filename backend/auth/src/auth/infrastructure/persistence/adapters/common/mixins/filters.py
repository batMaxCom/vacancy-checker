from typing import Any

from sqlalchemy import Select, Table

from auth.application.common.application_error import ApplicationError, ApplicationTypeError


class FilterMixin:
    @staticmethod
    def _add_filters(
        table: Table, query: Select, **filters: Any
    ) -> Select:
        """
        Add filters to query.
        Supported operators::
        __eq, __ne, __lt, __gt, __le, __ge, __in
        """
        operators = {
            "eq": lambda f, v: f == v,
            "ne": lambda f, v: f != v,
            "lt": lambda f, v: f < v,
            "gt": lambda f, v: f > v,
            "le": lambda f, v: f <= v,
            "ge": lambda f, v: f >= v,
            "in": lambda f, v: f.in_(v),
        }
        for key, value in filters.items():
            if value is None and "__" not in key:
                continue
            if "__" in key:
                col_name, op = key.split("__", 1)
                op_func = operators.get(op)
                if not op_func:
                    raise ApplicationError(
                        type=ApplicationTypeError.APPLICATION,
                        message=f"Unsupported filter operator: {op}"
                    )

                field = getattr(table.c, col_name)
                query = query.filter(op_func(field, value))
            else:
                field = getattr(table.c, key)
                query = query.filter(field == value)
        return query
