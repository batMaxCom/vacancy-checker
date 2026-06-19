from __future__ import annotations

import json
import re
from datetime import datetime
from typing import TYPE_CHECKING

import httpx

from search.application.common.dto import (
    EmploymentType,
    FoundVacancyDto,
    Salary,
    WorkFormat,
)
from search.application.ports.searcher import VacancySearchProvider

if TYPE_CHECKING:
    from search.domain.search_profile.value_objects import Keyword

_SNIPPET_LABELS: dict[str, str] = {
    "resp": "Обязанности",
    "req": "Требования",
    "cond": "Условия",
    "skill": "Навыки",
    "desc": "Описание",
}

_EMPLOYMENT_MAP: dict[str, EmploymentType] = {
    "FULL": EmploymentType.FULL_TIME,
    "PART": EmploymentType.PART_TIME,
    "PROJECT": EmploymentType.CONTRACT,
    "INTERNSHIP": EmploymentType.INTERNSHIP,
}

_WORK_FORMAT_MAP: dict[str, WorkFormat] = {
    "ON_SITE": WorkFormat.OFFICE,
    "REMOTE": WorkFormat.REMOTE,
    "HYBRID": WorkFormat.HYBRID,
}


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
    def _extract_json(html: str) -> dict | None:
        match = re.search(r'"vacancySearchResult"\s*:\s*(\{)', html)
        if not match:
            return None
        text = html[match.start(1):]
        depth = 0
        in_string = False
        escape = False
        end = 0
        for i, ch in enumerate(text):
            if escape:
                escape = False
                continue
            if ch == "\\":
                escape = True
                continue
            if ch == '"' and not escape:
                in_string = not in_string
                continue
            if not in_string:
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
        result = json.loads(text[:end])
        if not isinstance(result, dict):
            return None
        return result

    @staticmethod
    def _parse_salary(comp: dict | None) -> Salary | None:
        if not comp or "noCompensation" in comp:
            return None
        fr = comp.get("from")
        to = comp.get("to")
        if fr is None and to is None:
            return None
        if fr is not None and to is not None:
            return Salary(min_amount=str(fr), max_amount=str(to))
        value = fr if fr is not None else to
        return Salary(min_amount=str(value), max_amount=None)

    @staticmethod
    def _parse_employment_type(employment: dict | None) -> EmploymentType | None:
        if not employment:
            return None
        raw = employment.get("@type")
        if not isinstance(raw, str):
            return None
        return _EMPLOYMENT_MAP.get(raw)

    @staticmethod
    def _parse_work_format(work_formats: list | None) -> WorkFormat | None:
        if not work_formats:
            return None
        for entry in work_formats:
            if not isinstance(entry, dict):
                continue
            elements = entry.get("workFormatsElement")
            if isinstance(elements, list) and elements:
                raw = str(elements[0])
                wf = _WORK_FORMAT_MAP.get(raw)
                if wf:
                    return wf
        return None

    @staticmethod
    def _parse_datetime(value: object) -> datetime | None:
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None
        if isinstance(value, dict):
            raw = value.get("$")
            if isinstance(raw, str):
                try:
                    return datetime.fromisoformat(raw)
                except ValueError:
                    return None
        return None

    @staticmethod
    def _build_description(snippet: dict | None) -> str:
        if not snippet:
            return ""
        parts: list[str] = []
        for field in ("resp", "req", "cond", "skill", "desc"):
            val = snippet.get(field)
            if val and isinstance(val, str) and val.strip():
                label = _SNIPPET_LABELS.get(field, field)
                parts.append(f"{label}:\n{val.strip()}")
        return "\n\n".join(parts)

    @staticmethod
    def _get_location(v: dict) -> str | None:
        address = v.get("address")
        if isinstance(address, dict):
            display_name = address.get("displayName")
            if isinstance(display_name, str) and display_name:
                return display_name
        area = v.get("area")
        if isinstance(area, dict):
            name = area.get("name")
            if isinstance(name, str) and name:
                return name
        return None

    async def search(
        self,
        keywords: list[Keyword],
    ) -> list[FoundVacancyDto]:
        response = await self._client.get(
            self.BASE_URL,
            params={
                "text": " ".join(k.value for k in keywords),
                # "area": "99",
                "search_field": ["name", "company_name", "description"],
                "enable_snippets": "true",
            },
        )
        response.raise_for_status()

        data = self._extract_json(response.text)
        if not data:
            return []

        vacancies = data.get("vacancies") or []
        results: list[FoundVacancyDto] = []

        for v in vacancies:
            snippet = v.get("snippet") if isinstance(v.get("snippet"), dict) else {}
            company = v.get("company") if isinstance(v.get("company"), dict) else {}
            links = v.get("links") if isinstance(v.get("links"), dict) else {}

            results.append(
                FoundVacancyDto(
                    external_id=str(v["vacancyId"]),
                    title=v.get("name", ""),
                    description=self._build_description(snippet),
                    company_name=company.get("name", ""),
                    url=links.get("desktop", ""),
                    source="hh",
                    salary=self._parse_salary(v.get("compensation")),
                    location=self._get_location(v),
                    employment_type=self._parse_employment_type(
                        v.get("employment")
                    ),
                    work_format=self._parse_work_format(v.get("workFormats")),
                    published_at=self._parse_datetime(v.get("publicationTime")),
                    created_at=self._parse_datetime(v.get("creationTime")),
                    updated_at=self._parse_datetime(v.get("lastChangeTime")),
                )
            )

        return results
