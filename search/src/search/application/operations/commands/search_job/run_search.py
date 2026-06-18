import asyncio
from dataclasses import asdict, dataclass

from search.application.ports.broker.publisher import EventPublisher
from search.application.ports.cqrs import Command
from search.application.ports.cqrs.handlers import CommandHandler
from search.application.ports.id_generator import UUIDGenerator
from search.application.ports.searcher import VacancySearcher
from search.application.ports.time_provider import TimeProvider
from search.application.ports.transaction_manager import AsyncTransactionManager
from search.domain.search_job.entity import SearchJob
from search.domain.search_job.repository import SearchJobRepository
from search.domain.search_job.value_objects import SearchJobId
from search.domain.search_profile.repository import SearchProfileRepository
from search.domain.search_profile.value_objects import SearchProfileId


@dataclass(frozen=True, slots=True)
class RunSearchCommand(Command[SearchJobId]):
    profile_id: SearchProfileId


class RunSearchCommandHandler(CommandHandler[RunSearchCommand, SearchJobId]):
    def __init__(
        self,
        id_generator: UUIDGenerator,
        search_profile_repository: SearchProfileRepository,
        search_job_repository: SearchJobRepository,
        searcher: VacancySearcher,
        transaction_manager: AsyncTransactionManager,
        time_provider: TimeProvider,
        publisher: EventPublisher,
    ) -> None:
        self.__id_generator = id_generator
        self.__search_profile_repository = search_profile_repository
        self.__search_job_repository = search_job_repository
        self.__searcher = searcher
        self.__transaction_manager = transaction_manager
        self.__time_provider = time_provider
        self._publisher = publisher

    async def handle(self, command: RunSearchCommand) -> SearchJobId:
        profile = await self.__search_profile_repository.get(
            id=command.profile_id,
        )

        search_job = SearchJob(
            search_job_id=SearchJobId(self.__id_generator.next_id()),
            profile_id=profile.entity_id,
            started_at=self.__time_provider.current_time(),
        )

        search_job.start()
        await self.__search_job_repository.add(search_job)
        await self.__transaction_manager.commit()

        try:
            vacancies = await self.__searcher.search_by_profile(profile)
            search_job.complete(vacancies_found=len(vacancies))

        except Exception:
            search_job.fail()

        await self.__search_job_repository.update(search_job)
        await self.__transaction_manager.commit()
        await asyncio.gather(
            *(
                self._publisher.publish("new_vacancies", asdict(vacancy))
                for vacancy in vacancies
            ),
        )
        return search_job.entity_id
