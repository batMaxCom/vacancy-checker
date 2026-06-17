from typing import Any

from search.application.operations.commands.search_job import (
    RetrySearchJobCommand,
    RetrySearchJobCommandHandler,
    RunSearchCommand,
    RunSearchCommandHandler,
)
from search.application.operations.commands.search_profile import (
    ActivateSearchProfileCommand,
    ActivateSearchProfileCommandHandler,
    AddKeywordCommand,
    AddKeywordCommandHandler,
    CreateSearchProfileCommand,
    CreateSearchProfileCommandHandler,
    DeactivateSearchProfileCommand,
    DeactivateSearchProfileCommandHandler,
    DeleteSearchProfileCommand,
    DeleteSearchProfileCommandHandler,
    RemoveKeywordCommand,
    RemoveKeywordCommandHandler,
    UpdateSearchProfileCommand,
    UpdateSearchProfileCommandHandler,
)
from search.application.ports.cqrs import BaseRequest, RequestHandler
from search.infrastructure.mediator.registry import Registry

COMMAND_HANDLERS: list[tuple[type[BaseRequest[Any]], type[RequestHandler[Any, Any]]]] = [
    (RunSearchCommand, RunSearchCommandHandler),
    (RetrySearchJobCommand, RetrySearchJobCommandHandler),
    (ActivateSearchProfileCommand, ActivateSearchProfileCommandHandler),
    (AddKeywordCommand, AddKeywordCommandHandler),
    (CreateSearchProfileCommand, CreateSearchProfileCommandHandler),
    (DeactivateSearchProfileCommand, DeactivateSearchProfileCommandHandler),
    (DeleteSearchProfileCommand, DeleteSearchProfileCommandHandler),
    (RemoveKeywordCommand, RemoveKeywordCommandHandler),
    (UpdateSearchProfileCommand, UpdateSearchProfileCommandHandler),
]

def register_commands(registry: Registry) -> None:
    for command, handler in COMMAND_HANDLERS:
        registry.add_request_handler(command, handler)
