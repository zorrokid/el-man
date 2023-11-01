from dataclasses import dataclass
@dataclass
class AdaxTemperature:
    value: int

    def __init__(self, temperature: int):
        self.value = temperature
    
    def to_celsius(self) -> float:
        return self.value / 100.0

def adax_temperature_from_celcius(temperature: float) -> AdaxTemperature:
    return AdaxTemperature(int(temperature * 100.0))