"""Model to represent temperature in Adax API and to convert to and from celsius decimal."""
from dataclasses import dataclass
@dataclass
class AdaxTemperature:
    """Represents temperature in Adax API."""
    value: int

    def __init__(self, temperature: int):
        self.value = temperature

    def to_celsius(self) -> float:
        """Converts temperature to celsius decimal."""
        return self.value / 100.0

def adax_temperature_from_celcius(temperature: float) -> AdaxTemperature:
    """Converts temperature from celsius decimal to AdaxTempreature."""
    return AdaxTemperature(int(temperature * 100.0))
