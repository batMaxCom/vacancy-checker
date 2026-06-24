from dishka import Provider, Scope, alias
from sqlalchemy.orm import Session

from user.application.ports.transaction_manager import SyncTransactionManager


class CliApplicationAdaptersProvider(Provider):
    """Application adapter provider."""

    scope = Scope.APP

    transaction_manager = alias(Session, provides=SyncTransactionManager)
