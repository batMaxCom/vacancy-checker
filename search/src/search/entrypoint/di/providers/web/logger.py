from dishka import Provider, Scope, provide
from structlog import get_logger

from search.application.ports.logger import Logger
from search.infrastructure.adapters.logger import StructlogLogger


class LoggerAdapterProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_logger(self) -> Logger:
        return StructlogLogger(get_logger("application"))
