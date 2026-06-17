from dataclasses import dataclass


@dataclass(slots=True)
class Pagination:
    """Модель пагинации."""

    page_number: int
    page_size: int


@dataclass(frozen=True, slots=True)
class PaginationResult[TRecord]:
    """Модель представления страницы."""

    count_records: int
    page: int
    max_page_count: int
    records: list[TRecord]
