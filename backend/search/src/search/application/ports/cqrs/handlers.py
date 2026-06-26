from abc import ABC, abstractmethod
from typing import Any

from search.application.ports.cqrs.markers import BaseRequest, Command, Query


class RequestHandler[TRequest: BaseRequest[Any], TResponse](ABC):
    @abstractmethod
    async def handle(self, request: TRequest) -> TResponse: ...


class CommandHandler[TCommand: Command[Any], TResponse](RequestHandler[TCommand, TResponse]):
    @abstractmethod
    async def handle(self, command: TCommand) -> TResponse: ...


class QueryHandler[TQuery: Query[Any], TResponse](RequestHandler[TQuery, TResponse]):
    @abstractmethod
    async def handle(self, query: TQuery) -> TResponse: ...
