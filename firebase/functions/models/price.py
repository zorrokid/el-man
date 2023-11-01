"""Contains class to represent price in certain point of time."""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Price:
    """Represents price in certain point of time."""
    time: datetime
    price: float

    def get_price_key(self):
        """Returns price key."""""
        return self.create_price_key(self.time)

    @staticmethod
    def create_price_key(time: datetime):
        """Creates price key from time."""
        return time.strftime("%Y%m%d%H00")
