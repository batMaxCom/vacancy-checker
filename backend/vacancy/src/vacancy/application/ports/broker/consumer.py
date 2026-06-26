from abc import ABC, abstractmethod


class EventConsumer(ABC):

    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def stop(self) -> None:
        ...
