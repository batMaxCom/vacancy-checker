import httpx
from bs4 import BeautifulSoup, Tag

from search.application.common.dto import FoundVacancyDto
from search.application.ports.searcher import VacancySearchProvider
from search.domain.search_profile.value_objects import Keyword


class HHSearchProvider(VacancySearchProvider):
    BASE_URL = "https://hh.ru/search/vacancy"

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            },
            follow_redirects=True,
        )

    @staticmethod
    def _text(tag: Tag | None) -> str:
        return tag.get_text(strip=False).replace("\u00a0", " ").strip() if tag else ""

    async def search(
        self,
        keywords: list[Keyword],
    ) -> list[FoundVacancyDto]:
        response = await self._client.get(
            self.BASE_URL,
            params={
                "text": " ".join(k.value for k in keywords),
                "area": "99",
                # "professional_role": "96",
                "search_field": ["name", "company_name", "description"],
                "enable_snippets": "true",
            },
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        cards = soup.select("[class*=vacancy-card]")

        results: list[FoundVacancyDto] = []
        for card in cards:
            id_attr = card.get("id")
            if not isinstance(id_attr, str):
                continue
            if not id_attr.isdigit():
                continue

            title_tag = card.select_one("[data-qa=serp-item__title-text]")
            title = self._text(title_tag)

            url_tag = card.select_one("[data-qa=serp-item__title]")
            href = url_tag.get("href") if isinstance(url_tag, Tag) else ""
            full_url = href if isinstance(href, str) and href.startswith("http") else f"https://hh.ru{href}"

            company_tag = card.select_one("[data-qa=vacancy-serp__vacancy-employer-text]")
            company = self._text(company_tag)

            snippet_parts: list[str] = []
            salary_tag = card.select_one("[class*=compensation]")
            if isinstance(salary_tag, Tag):
                snippet_parts.append(self._text(salary_tag))
            for snippet_qa in (
                "vacancy-serp__vacancy_snippet_responsibility",
                "vacancy-serp__vacancy_snippet_requirement",
            ):
                tag = card.select_one(f"[data-qa={snippet_qa}]")
                if isinstance(tag, Tag):
                    snippet_parts.append(self._text(tag))
            description = "\n".join(snippet_parts)

            results.append(
                FoundVacancyDto(
                    external_id=id_attr,
                    title=title,
                    description=description,
                    company=company,
                    url=full_url,
                    source="hh",
                )
            )

        return results
