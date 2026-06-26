from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Salary:
    min_amount: Decimal | None
    max_amount: Decimal | None
