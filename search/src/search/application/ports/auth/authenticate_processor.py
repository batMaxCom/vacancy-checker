from abc import ABC, abstractmethod


class AuthenticateProcessor(ABC):
    @abstractmethod
    async def process(self) -> None: ...
