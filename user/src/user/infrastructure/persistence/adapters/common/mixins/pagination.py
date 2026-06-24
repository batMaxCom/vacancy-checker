import math

from sqlalchemy import Select, func

from user.application.common.dto import Pagination, PaginationResult


class PaginationMixin:
    @staticmethod
    def _add_count_records_column(query: Select) -> Select:
        """Получить количество записей."""
        return query.add_columns(func.count().over().label("count_records"))

    @staticmethod
    def _add_query_offset_and_limit(
        query: Select, page_number: int, page_size: int
    ) -> Select:
        """Смещение и ограничение запроса."""
        page_number = page_number - 1 if page_number > 0 else page_number
        return query.offset(page_number * page_size).limit(page_size)

    @staticmethod
    def _get_pagination_result(
            pagination: Pagination, records: list, count_records: int
    ) -> PaginationResult:
        max_page_count = (
            math.ceil(count_records / pagination.page_size) if count_records else 0
        )
        return PaginationResult(
            page=pagination.page_number,
            max_page_count=max_page_count,
            count_records=count_records,
            records=records,
        )
