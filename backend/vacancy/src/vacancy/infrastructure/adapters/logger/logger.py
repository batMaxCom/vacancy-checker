from typing import Any

from vacancy.application.ports import Logger


class StructlogLogger(Logger):
    def __init__(self, logger: Any) -> None:
        self._logger = logger

    async def ainfo(self, event: str, *args: Any, **kw: Any) -> Any:
        self._logger.info(event, *args, **kw)

    def info(self, event: str, *args: Any, **kw: Any) -> Any:
        self._logger.info(event, *args, **kw)

    async def awarning(self, event: str, *args: Any, **kw: Any) -> Any:
        await self._logger.awarning(event, *args, **kw)

    def error(self, event: str | None = None, *args: Any, **kw: Any) -> Any:
        self._logger.error(event, *args, **kw)

    async def aexception(self, event: str, *args: Any, **kw: Any) -> Any:
        await self._logger.aexception(event, *args, **kw)
