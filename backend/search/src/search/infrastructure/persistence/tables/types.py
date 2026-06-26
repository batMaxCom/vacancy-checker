from typing import Any

from sqlalchemy import JSON, String
from sqlalchemy.types import TypeDecorator

from search.domain.search_job.value_objects import SearchJobStatus
from search.domain.search_profile.value_objects import Keyword


class KeywordsColumn(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value: Any | None, dialect: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, list):
            return [k.value if isinstance(k, Keyword) else k for k in value]
        return value

    def process_result_value(self, value: Any | None, dialect: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, list):
            return [Keyword(k) if isinstance(k, str) else k for k in value]
        return value


class SearchJobStatusColumn(TypeDecorator):
    impl = String

    def process_bind_param(self, value: Any | None, dialect: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, SearchJobStatus):
            return value.value
        return value

    def process_result_value(self, value: Any | None, dialect: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            return SearchJobStatus(value)
        return value
