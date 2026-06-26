from abc import ABC, abstractmethod

from vacancy.application.ports.cqrs import RequestHandler

type Handler = RequestHandler


class Resolver(ABC):
    """Base class for all resolvers."""

    @abstractmethod
    async def resolve[TDependency: Handler](
        self, dependency_type: type[TDependency]
    ) -> TDependency: ...
