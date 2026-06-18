from typing import Protocol


class EventPublisher(Protocol):
    async def publish(self, topic: str, payload: dict) -> None:
        ...
