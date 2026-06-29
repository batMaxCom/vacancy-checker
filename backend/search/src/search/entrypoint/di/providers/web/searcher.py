from dishka import Provider, Scope, provide

from search.application.ports.searcher import VacancySearcher, VacancySearchProvider
from search.entrypoint.web.config import TgConfig
from search.infrastructure.adapters.searcher.search_providers import (
    HabrCareerSearchProvider,
    HHSearchProvider,
    TgSearchProvider,
)
from search.infrastructure.adapters.searcher.vacancy_searcher import MultiSourceVacancySearcher


class SearcherProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_vacancy_searcher(self) -> VacancySearcher:
        providers: list[VacancySearchProvider] = [
            HHSearchProvider(),
            HabrCareerSearchProvider(),
        ]

        tg_config = TgConfig.from_env()
        if tg_config.api_id and tg_config.api_hash and tg_config.channels:
            providers.append(
                TgSearchProvider(
                    api_id=tg_config.api_id,
                    api_hash=tg_config.api_hash,
                    channels=tg_config.channels,
                    session_name=tg_config.session_name,
                ),
            )

        return MultiSourceVacancySearcher(providers=providers)
