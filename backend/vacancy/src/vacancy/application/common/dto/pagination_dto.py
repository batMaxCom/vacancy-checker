from dataclasses import dataclass


@dataclass(slots=True)
class PaginationDto:
    """Модель пагинации."""

    page_number: int
    page_size: int


@dataclass(frozen=True, slots=True)
class PaginationResultDto[TRecord]:
    """Модель представления страницы."""

    count_records: int
    page: int
    max_page_count: int
    records: list[TRecord]
