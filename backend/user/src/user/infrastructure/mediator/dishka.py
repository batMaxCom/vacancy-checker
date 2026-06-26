from typing import TypeVar, cast

from dishka import AsyncContainer

from user.application.ports.cqrs import Handler, Resolver

TDependency = TypeVar("TDependency", bound=Handler)


class DishkaResolver(Resolver):
    """Resolver for HTTP requests."""

    def __init__(self, container: AsyncContainer) -> None:
        self._container = container

    async def resolve(self, dependency_type: type[TDependency]) -> TDependency:
        return cast(TDependency, await self._container.get(dependency_type))
