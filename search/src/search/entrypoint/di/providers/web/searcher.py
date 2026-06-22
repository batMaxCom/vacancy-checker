from dishka import Provider, Scope, provide

from search.application.ports.searcher import VacancySearcher
from search.infrastructure.adapters.searcher.search_providers.habr_career_search_provider import (
    HabrCareerSearchProvider,
)
from search.infrastructure.adapters.searcher.search_providers.hh_search_provider import (
    HHSearchProvider,
)
from search.infrastructure.adapters.searcher.vacancy_searcher import MultiSourceVacancySearcher


class SearcherProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_vacancy_searcher(self) -> VacancySearcher:
        return MultiSourceVacancySearcher(
            providers=[
                HHSearchProvider(),
                HabrCareerSearchProvider()
            ],
        )
