from abc import ABC, abstractmethod
from typing import Any


class Logger(ABC):
    @abstractmethod
    async def ainfo(self, event: str, *args: Any, **kw: Any) -> Any: ...

    @abstractmethod
    def info(self, event: str, *args: Any, **kw: Any) -> Any: ...

    @abstractmethod
    async def awarning(self, event: str, *args: Any, **kw: Any) -> Any: ...

    @abstractmethod
    def error(self, event: str | None = None, *args: Any, **kw: Any) -> Any: ...

    @abstractmethod
    async def aexception(self, event: str, *args: Any, **kw: Any) -> Any: ...
