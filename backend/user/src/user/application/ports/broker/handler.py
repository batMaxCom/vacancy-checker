from abc import ABC, abstractmethod
from typing import Any


class EventHandler(ABC):
    @abstractmethod
    async def handle(
        self,
        event_type: str,
        payload: dict[str, Any],
    ) -> None: ...
