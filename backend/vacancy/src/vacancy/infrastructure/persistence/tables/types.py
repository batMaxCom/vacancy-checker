from enum import Enum

from sqlalchemy import String, TypeDecorator


class EnumAsString(TypeDecorator):
    impl = String

    def __init__(self, enum_type: type[Enum], **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._enum_type = enum_type

    def process_bind_param(self, value: object | None, dialect: object) -> str | None:
        if value is None:
            return None
        return value.name if isinstance(value, Enum) else str(value)

    def process_result_value(self, value: str | None, dialect: object) -> Enum | None:
        if value is None:
            return None
        return self._enum_type[value]
