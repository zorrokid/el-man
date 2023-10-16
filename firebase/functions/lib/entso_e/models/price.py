from dataclasses import dataclass
from datetime import datetime

@dataclass
class Price:
    time: datetime
    price: float

    def get_price_key(self):
        return self.time.strftime("%Y%m%d%H%M")