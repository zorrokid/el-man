from dataclasses import dataclass
from datetime import datetime

@dataclass
class Price:
    time: datetime
    price: float

    def get_price_key(self):
        return self.create_price_key(self.price)

    @staticmethod
    def create_price_key(time: datetime):
        return time.strftime("%Y%m%d%H%M") 
