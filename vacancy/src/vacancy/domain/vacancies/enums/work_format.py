from enum import Enum, auto


class VacancyStatus(Enum):
    ACTIVE = auto()
    ARCHIVED = auto()
    DELETED = auto()
