from abc import ABC, abstractmethod

from auth.application.ports.cqrs import BaseRequest


class Sender(ABC):
    """Send request."""

    @abstractmethod
    async def send[TResponse](self, request: BaseRequest[TResponse]) -> TResponse: ...
