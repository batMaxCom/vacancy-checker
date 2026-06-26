import asyncio

from search.application.common.dto import FoundVacancyDto
from search.application.ports.searcher import VacancySearchProvider
from search.application.ports.searcher.vacancy_searcher import VacancySearcher
from search.domain.search_profile.entity import SearchProfile


class MultiSourceVacancySearcher(VacancySearcher):
    def __init__(
        self,
        providers: list[VacancySearchProvider],
    ) -> None:
        self._providers = providers

    async def search_by_profile(
        self,
        profile: SearchProfile,
    ) -> list[FoundVacancyDto]:

        tasks = [
            provider.search(profile.keywords)
            for provider in self._providers
        ]

        results = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

        vacancies: list[FoundVacancyDto] = []

        for result in results:
            if isinstance(result, BaseException):
                continue

            vacancies.extend(result)

        return vacancies
