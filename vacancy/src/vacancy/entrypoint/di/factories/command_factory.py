from typing import Any

from vacancy.application.operations.commands.source import (
    CreateSourceCommand,
    CreateSourceCommandHandler,
    UpdateSourceCommand,
    UpdateSourceCommandHandler,
)
from vacancy.application.operations.commands.vacancy import (
    CreateVacancyCommand,
    CreateVacancyCommandHandler,
    UpdateVacancyCommand,
    UpdateVacancyCommandHandler,
)
from vacancy.application.ports.cqrs import BaseRequest, RequestHandler
from vacancy.infrastructure.mediator.registry import Registry

COMMAND_HANDLERS: list[tuple[type[BaseRequest[Any]], type[RequestHandler[Any, Any]]]] = [
    (CreateSourceCommand, CreateSourceCommandHandler),
    (UpdateSourceCommand, UpdateSourceCommandHandler),
    (CreateVacancyCommand, CreateVacancyCommandHandler),
    (UpdateVacancyCommand, UpdateVacancyCommandHandler),
]

def register_commands(registry: Registry) -> None:
    for command, handler in COMMAND_HANDLERS:
        registry.add_request_handler(command, handler)
