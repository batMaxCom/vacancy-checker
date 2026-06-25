from typing import Any
from uuid import UUID

from dishka import AsyncContainer, Scope

from user.application.operations.commands.user.create_user import CreateUserCommand
from user.application.ports.broker import EventHandler
from user.application.ports.cqrs import Command, Sender
from user.application.ports.logger import Logger
from user.domain.user.value_objects import Email, FirstName, LastName, UserId


class RabbitMQEventHandler(EventHandler):

    def __init__(self, container: AsyncContainer, logger: Logger) -> None:
        self.__container = container
        self._logger = logger

    async def handle(self, event_type: str, payload: dict[str, Any]) -> None:
        command = self._map(event_type, payload)
        async with self.__container(scope=Scope.REQUEST) as request_container:
            sender = await request_container.get(Sender)
            await sender.send(command)
        await self._logger.ainfo(
            event="RABBITMQ_EVENT_HANDLER",
            event_type=event_type,
        )

    def _map(self, event_type: str, payload: dict[str, Any]) -> Command:
        if event_type == "user.created":
            return self._to_create_user_command(payload)
        raise ValueError(f"Unknown event type: {event_type}")

    @staticmethod
    def _to_create_user_command(payload: dict[str, Any]) -> CreateUserCommand:
        return CreateUserCommand(
            user_id=UserId(UUID(payload["user_id"])),
            email=Email(payload["email"]),
            first_name=FirstName(payload["first_name"]),
            last_name=LastName(payload["last_name"]),
        )
