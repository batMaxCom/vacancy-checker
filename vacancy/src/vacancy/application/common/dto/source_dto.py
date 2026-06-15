from dataclasses import dataclass

from vacancy.domain.sources.value_objects import SourceId


@dataclass(frozen=True, slots=True)
class SourceDto:
    source_id: SourceId
    name: str
    base_url: str
    is_active: bool
