from typing import NewType

from vacancy.application.ports.logger.logger import Logger

BrokerLogger = NewType("BrokerLogger", Logger)
# WSLogger = NewType("WSLogger", Logger)
CQRSLogger = NewType("CQRSLogger", Logger)
# AuthLogger = NewType("AuthLogger", Logger)
