from dishka import Provider, Scope, provide
from structlog import get_logger

from vacancy.application.ports.logger import Logger
from vacancy.infrastructure.adapters.logger import StructlogLogger


class LoggerAdapterProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_logger(self) -> Logger:
        return StructlogLogger(get_logger("application"))
