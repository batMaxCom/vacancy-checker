import uuid

from search.application.ports import UUIDGenerator


class UUIDGeneratorImpl(UUIDGenerator):
    """Class for generating UUIDs."""

    def next_id(self) -> uuid.UUID:
        return uuid.uuid4()
