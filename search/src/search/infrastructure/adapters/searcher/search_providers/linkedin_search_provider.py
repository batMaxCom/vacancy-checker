from search.application.common.dto import FoundVacancyDto
from search.application.ports.searcher import VacancySearchProvider
from search.domain.search_profile.value_objects import Keyword


class LinkedInSearchProvider(VacancySearchProvider):
    async def search(
        self,
        keywords: list[Keyword],
    ) -> list[FoundVacancyDto]:
        return [
            FoundVacancyDto(
                external_id="123",
                title="Python Developer",
                description="...",
                company="Google",
                url="https://linkedin.com/job/123",
                source="linkedin",
            )
        ]
