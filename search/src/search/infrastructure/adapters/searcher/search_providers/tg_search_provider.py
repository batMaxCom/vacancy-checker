from __future__ import annotations

import asyncio
import re
from typing import TYPE_CHECKING

from telethon import TelegramClient  # type: ignore[import-untyped]

from search.application.common.dto import FoundVacancyDto, Salary
from search.application.ports.searcher import VacancySearchProvider

if TYPE_CHECKING:
    from search.domain.search_profile.value_objects import Keyword


_SALARY_PATTERNS: list[re.Pattern[str]] = [
    re.compile(
        r"(?:от\s*)?(\d[\d\s]*)(?:\s*до\s*(\d[\d\s]*))?\s*(?:руб|₽|rub)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(\d[\d\s]*)\s*(?:[–—\-])\s*(\d[\d\s]*)\s*(?:руб|₽|rub)",
        re.IGNORECASE,
    ),
    re.compile(
        r"з/п[:\s]*(\d[\d\s]*)(?:\s*(?:[–—\-])\s*(\d[\d\s]*))?\s*(?:руб|₽|rub)",
        re.IGNORECASE,
    ),
    re.compile(
        r"зарплат[а-я][:\s]*(\d[\d\s]*)(?:\s*(?:[–—\-])\s*(\d[\d\s]*))?\s*(?:руб|₽|rub)",
        re.IGNORECASE,
    ),
]


def _extract_salary(text: str) -> Salary | None:
    for pattern in _SALARY_PATTERNS:
        match = pattern.search(text)
        if match:
            groups = match.groups()
            min_raw = groups[0] if groups else None
            max_raw = groups[1] if len(groups) > 1 else None

            min_val = re.sub(r"\s+", "", min_raw) if min_raw else None
            max_val = re.sub(r"\s+", "", max_raw) if max_raw else None

            if not min_val and not max_val:
                continue

            return Salary(
                min_amount=min_val or None,
                max_amount=max_val or None,
            )
    return None


class TgSearchProvider(VacancySearchProvider):
    _CONCURRENCY = 3
    _MAX_MESSAGES_PER_SEARCH = 50

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        channels: list[str],
        session_name: str = "tg_search_session",
    ) -> None:
        self._api_id = api_id
        self._api_hash = api_hash
        self._channels = channels
        self._session_name = session_name

    async def _search_channel(
        self,
        client: TelegramClient,
        channel: str,
        keyword: str,
    ) -> list[FoundVacancyDto]:
        results: list[FoundVacancyDto] = []
        seen: set[int] = set()

        async for message in client.iter_messages(
            channel,
            search=keyword,
        ):
            if not message.text or message.id in seen:
                continue
            if len(results) >= self._MAX_MESSAGES_PER_SEARCH:
                break
            seen.add(message.id)

            text = message.text.strip()
            lines = text.split("\n", 1)
            title = lines[0].strip()
            description = lines[1].strip() if len(lines) > 1 else ""

            salary = _extract_salary(text)
            channel_tag = channel.strip("@")
            url = f"https://t.me/{channel_tag}/{message.id}"

            results.append(FoundVacancyDto(
                external_id=f"{channel_tag}:{message.id}",
                title=title,
                description=description,
                company_name="",
                url=url,
                source=f"tg:{channel_tag}",
                source_url=f"https://t.me/{channel_tag}",
                salary=salary,
                location=None,
                employment_type=None,
                work_format=None,
                published_at=message.date,
                created_at=None,
                updated_at=None,
            ))

        return results

    async def search(
        self,
        keywords: list[Keyword],
    ) -> list[FoundVacancyDto]:
        if not self._channels or not keywords:
            return []
        client = TelegramClient(
            self._session_name,
            api_id=self._api_id,
            api_hash=self._api_hash,
            lang_code="ru",
            system_lang_code="ru-RU"
        )
        await client.start()

        try:
            all_results: list[FoundVacancyDto] = []
            seen: set[str] = set()
            sem = asyncio.Semaphore(self._CONCURRENCY)

            async def search_channel(ch: str, kw: str) -> list[FoundVacancyDto]:
                async with sem:
                    return await self._search_channel(client, ch, kw)

            tasks = [
                search_channel(channel, keyword.value)
                for channel in self._channels
                for keyword in keywords
            ]

            results: list[list[FoundVacancyDto] | BaseException] = await asyncio.gather(
                *tasks,
                return_exceptions=True,
            )

            for result in results:
                if isinstance(result, BaseException):
                    continue
                for dto in result:
                    if dto.external_id not in seen:
                        seen.add(dto.external_id)
                        all_results.append(dto)

            return all_results
        finally:
            await client.stop()

