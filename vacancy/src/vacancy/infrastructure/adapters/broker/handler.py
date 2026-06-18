from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

from dishka import AsyncContainer, Scope

from vacancy.application.operations.commands.vacancy.create_vacancy import (
    CreateVacancyCommand,
)
from vacancy.application.ports.broker import EventHandler
from vacancy.application.ports.cqrs import Command, Sender
from vacancy.application.ports.logger import BrokerLogger
from vacancy.domain.vacancies.enums import EmploymentType, WorkFormat
from vacancy.domain.vacancies.value_objects import Salary, VacancyId


class KafkaEventHandler(EventHandler):

    def __init__(self, container: AsyncContainer, logger: BrokerLogger) -> None:
        self.__container = container
        self._logger = logger

    async def handle(self, event_type: str, payload: dict[str, Any]) -> None:
        command = self._map(event_type, payload)
        async with self.__container(scope=Scope.REQUEST) as request_container:
            sender = await request_container.get(
                Sender
            )
            await sender.send(command)
        await self._logger.ainfo(
            event="KAFKA_EVENT_HANDLER",
            event_type=event_type,
        )

    def _map(self, event_type: str, payload: dict[str, Any]) -> Command:
        if event_type == "vacancy.created":
            return self._to_create_vacancy_command(payload)
        raise ValueError(f"Unknown event type: {event_type}")

    @staticmethod
    def _to_create_vacancy_command(
        payload: dict[str, Any]
    ) -> CreateVacancyCommand:
        salary = None
        salary_min = payload.get("salary_min") or payload.get("salary", {}).get(
            "min_amount"
        )
        salary_max = payload.get("salary_max") or payload.get("salary", {}).get(
            "max_amount"
        )
        if salary_min is not None or salary_max is not None:
            salary = Salary(
                min_amount=Decimal(str(salary_min))
                if salary_min is not None
                else None,
                max_amount=Decimal(str(salary_max))
                if salary_max is not None
                else None,
            )
        employment_type = (
            EmploymentType[payload["employment_type"]]
            if payload.get("employment_type") else None
        )
        work_format = (
            WorkFormat[payload["work_format"]]
            if payload.get("work_format") else None
        )
        published_at = (
            datetime.fromisoformat(payload["published_at"])
            if payload.get("published_at") else None
        )

        return CreateVacancyCommand(
            vacancy_id=VacancyId(uuid4()),
            external_id=payload.get("external_id"),
            title=payload["title"],
            description=payload["description"],
            company_name=payload.get("company_name") or "",
            employment_type=employment_type,
            work_format=work_format,
            salary=salary,
            location=payload.get("location"),
            url=payload["url"],
            published_at=published_at
        )
