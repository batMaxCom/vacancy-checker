from abc import ABC, abstractmethod
from typing import Any


class EventProducer(ABC):
    @abstractmethod
    async def publish(self, routing_key: str, message: dict[str, Any]) -> None: ...
