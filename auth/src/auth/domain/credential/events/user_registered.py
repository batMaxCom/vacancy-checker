from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UserRegisteredEvent:
    user_id: int
    email: str
    first_name: str
    last_name: str