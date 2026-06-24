from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserDTO:
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    status: str


@dataclass(frozen=True, slots=True)
class UserBriefDTO:
    id: str
    email: str
    first_name: str
    last_name: str
