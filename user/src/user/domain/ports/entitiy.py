from collections.abc import Hashable


class Entity[TEntityId: Hashable]:
    """Base class for all entities"""

    def __init__(self, entity_id: TEntityId) -> None:
        self._entity_id = entity_id

    @property
    def entity_id(self) -> TEntityId:
        return self._entity_id

    @entity_id.setter
    def entity_id(self, value: TEntityId) -> None:
        """Entity id cannot be changed"""
        raise AttributeError("Entity id cannot be changed")

    def __eq__(self, other: object) -> bool:
        """Entities are equal if their ids are equal"""
        if not isinstance(other, Entity):
            return NotImplemented
        return bool(self.entity_id == other.entity_id)

    def __hash__(self) -> int:
        """Hash is based on entity id"""
        return hash(self.entity_id)
