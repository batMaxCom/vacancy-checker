from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SelectItemDto[TValue]:
    value: TValue
    label: str
