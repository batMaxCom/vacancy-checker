from __future__ import annotations

import asyncio
import re
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import httpx
from bs4 import BeautifulSoup, Tag

from search.application.common.dto import FoundVacancyDto, Salary
from search.application.ports.searcher import VacancySearchProvider

if TYPE_CHECKING:
    from search.domain.search_profile.value_objects import Keyword


_RELATIVE_DATE_PATTERNS: list[tuple[re.Pattern[str], int]] = [
    (re.compile(r"только что"), 0),
    (re.compile(r"(\d+)\s+минут\w+\s+назад"), 1),
    (re.compile(r"(\d+)\s+час\w+\s+назад"), 60),
    (re.compile(r"сегодня"), 0),
    (re.compile(r"вчера"), 1440),
    (re.compile(r"(\d+)\s+день\w+\s+назад"), 1440),
    (re.compile(r"(\d+)\s+дн\w+\s+назад"), 1440),
    (re.compile(r"(\d+)\s+недел\w+\s+назад"), 10080),
]


def _parse_relative_date(text: str) -> datetime | None:
    now = datetime.now(timezone.utc)
    for pattern, multiplier in _RELATIVE_DATE_PATTERNS:
        match = pattern.search(text.strip().lower())
        if match:
            groups = match.groups()
            if groups:
                try:
                    minutes = int(groups[0]) * multiplier
                    return now - timedelta(minutes=minutes)
                except (ValueError, IndexError):
                    return now
            return now
    return None


def _parse_salary(text: str) -> Salary | None:
    cleaned = text.strip().replace("\u2009", "").replace(" ", "")
    if not cleaned or cleaned == "неуказана":
        return None
    parts = re.split(r"[–—\-]", cleaned)
    min_part = parts[0].strip()
    if len(parts) == 2:
        max_part = parts[1].strip()
        min_val = re.sub(r"[^\d]", "", min_part)
        max_val = re.sub(r"[^\d]", "", max_part)
        if min_val or max_val:
            return Salary(
                min_amount=min_val or None,
                max_amount=max_val or None,
            )
    if min_part:
        val = re.sub(r"[^\d]", "", min_part)
        if val:
            return Salary(min_amount=val, max_amount=None)
    return None


class HabrCareerSearchProvider(VacancySearchProvider):
    BASE_URL = "https://career.habr.com/vacancies"
    _CONCURRENCY = 3

    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client = client or httpx.AsyncClient(
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            },
            follow_redirects=True,
        )

    @staticmethod
    def _parse_vacancy_card(card: Tag) -> FoundVacancyDto | None:
        title_link = card.select_one("a.vacancy-card__title-link")
        if not title_link or not isinstance(title_link, Tag):
            return None
        title = title_link.get_text(strip=True)
        href = str(title_link.get("href", ""))
        external_id = href.rstrip("/").rsplit("/", 1)[-1] if href else ""
        url = f"https://career.habr.com{href}" if href else ""

        company_el = card.select_one("div.vacancy-card__company-title")
        company_name = company_el.get_text(strip=True) if company_el else ""

        salary_el = card.select_one("div.vacancy-card__salary")
        salary = _parse_salary(salary_el.get_text(strip=True)) if salary_el else None

        meta_el = card.select_one("div.vacancy-card__meta")
        location: str | None = None
        published_at: datetime | None = None
        if meta_el:
            meta_text = meta_el.get_text(" ", strip=True)
            date_match = re.search(
                r"(только что|\d+\s+минут\w+\s+назад|\d+\s+час\w+\s+назад|"
                r"сегодня|вчера|\d+\s+дн\w+\s+назад|\d+\s+недел\w+\s+назад)",
                meta_text,
            )
            if date_match:
                published_at = _parse_relative_date(date_match.group(1))
            location_text = meta_text
            if date_match:
                location_text = meta_text.replace(date_match.group(1), "").strip()
            location_text = re.sub(r"[•·,]\s*", "", location_text).strip()
            if location_text:
                location = location_text

        if not external_id:
            return None

        return FoundVacancyDto(
            external_id=external_id,
            title=title,
            description="",
            company_name=company_name,
            url=url,
            source="career.habr.com",
            source_url="https://career.habr.com",
            salary=salary,
            location=location,
            employment_type=None,
            work_format=None,
            published_at=published_at,
            created_at=None,
            updated_at=None,
        )

    async def _parse_page(self, params: dict[str, str], page: int) -> list[FoundVacancyDto]:
        response = await self._client.get(
            self.BASE_URL,
            params={**params, "page": str(page)},
        )
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "lxml")
        return [
            dto for c in soup.select("div.vacancy-card")
            if isinstance(c, Tag) and (dto := self._parse_vacancy_card(c)) is not None
        ]

    async def search(
        self,
        keywords: list[Keyword],
    ) -> list[FoundVacancyDto]:
        text = " ".join(k.value for k in keywords)
        params: dict[str, str] = {"q": text, "type": "all"}
        all_vacancies: list[FoundVacancyDto] = []
        seen: set[str] = set()

        sem = asyncio.Semaphore(self._CONCURRENCY)

        async def fetch(p: int) -> list[FoundVacancyDto]:
            async with sem:
                return await self._parse_page(params, p)

        page = 1
        while True:
            tasks = [fetch(p) for p in range(page, page + self._CONCURRENCY)]
            results: list[list[FoundVacancyDto] | BaseException] = await asyncio.gather(
                *tasks, return_exceptions=True,
            )

            any_data = False
            for result in results:
                if isinstance(result, BaseException):
                    continue
                if result:
                    any_data = True
                    for dto in result:
                        if dto.external_id not in seen:
                            seen.add(dto.external_id)
                            all_vacancies.append(dto)

            if not any_data:
                break

            page += self._CONCURRENCY

        return all_vacancies
