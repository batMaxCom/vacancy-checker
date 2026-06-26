from vacancy.domain.ports import Entity
from vacancy.domain.sources.value_objects import SourceId


class Source(Entity[SourceId]):
    def __init__(
        self,
        source_id: SourceId,
        name: str,
        base_url: str,
        is_active: bool
    ) -> None:
        super().__init__(source_id)
        self._name = name
        self._base_url = base_url
        self._is_active = is_active

    @property
    def name(self) -> str:
        return self._name

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def is_active(self) -> bool:
        return self._is_active

    def rename(self, name: str) -> None:
        self._name = name

    def set_base_url(self, base_url: str) -> None:
        self._base_url = base_url

    def activate(self) -> None:
        self._is_active = True

    def deactivate(self) -> None:
        self._is_active = False

    @classmethod
    def create(
        cls,
        source_id: SourceId,
        name: str,
        base_url: str = "",
        is_active: bool = True,
    ) -> "Source":
        return cls(
            source_id=source_id,
            name=name,
            base_url=base_url,
            is_active=is_active,
        )

    @classmethod
    def restore(
        cls,
        source_id: SourceId,
        name: str,
        base_url: str,
        is_active: bool,
    ) -> "Source":
        return cls(
            source_id=source_id,
            name=name,
            base_url=base_url,
            is_active=is_active,
        )
