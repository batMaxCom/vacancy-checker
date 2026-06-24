from dataclasses import dataclass
from os import environ
from typing import Self


@dataclass(frozen=True)
class TgConfig:
    api_id: int
    api_hash: str
    channels: list[str]
    session_name: str

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            api_id=int(environ.get("TG_API_ID", "0")),
            api_hash=environ.get("TG_API_HASH", ""),
            channels=[
                ch.strip()
                for ch in environ.get("TG_CHANNELS", "").split(",")
                if ch.strip()
            ],
            session_name=environ.get("TG_SESSION_NAME", "tg_search_session"),
        )
