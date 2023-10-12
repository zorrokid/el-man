from dataclasses import dataclass
from datetime import datetime

@dataclass
class Price:
    time: datetime
    price: float