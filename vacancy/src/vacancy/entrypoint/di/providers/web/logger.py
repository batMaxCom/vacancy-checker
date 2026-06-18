import structlog
from dishka import Provider, Scope, provide
from structlog import get_logger

from vacancy.application.ports.logger import BrokerLogger, CQRSLogger, Logger
from vacancy.infrastructure.adapters.logger import StructlogLogger


class LoggerAdapterProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_logger(self) -> Logger:
        return StructlogLogger(get_logger("application"))

    @provide
    def broker_logger(self) -> BrokerLogger:
        return BrokerLogger(StructlogLogger(structlog.get_logger("broker")))


    @provide
    def cqrs_logger(self) -> CQRSLogger:
        return CQRSLogger(StructlogLogger(structlog.get_logger("cqrs")))
