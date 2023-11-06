"""Contains HeatingSettings classi and helper functions."""
from dataclasses import dataclass

DEFAULT_MAX_PRICE = 5
DEFAULT_MIN_PRICE = 2
DEFAULT_HEATING_ENABLED = True
DEFAULT_MAX_TEMPERATURE = 20
DEFAULT_MIN_TEMPERATURE = 5
DEFAULT_MID_TEMPERATURE = 10

@dataclass
class HeatingSettings:
    """Represents heating settings."""
    max_price: int
    low_price: int
    heating_enabled: bool
    heating_max_temperature: int
    heating_min_temperature: int
    heating_mid_temperature: int

    def to_dict(self):
        """Converts heating settings to dictionary."""
        return {
            'maxPrice': self.max_price,
            'lowPrice': self.low_price,
            'heatingEnabled': self.heating_enabled,
            'heatingMaxTemperature': self.heating_max_temperature,
            'heatingMinTemperature': self.heating_min_temperature,
            'heatingMidTemperature': self.heating_mid_temperature
        }

def heating_settings_from_dict(source: dict) -> HeatingSettings:
    """Converts dictionary to HeatingSettings."""
    return HeatingSettings(
        int(source['maxPrice']),
        int(source['lowPrice']),
        bool(source['heatingEnabled']),
        int(source['heatingMaxTemperature']),
        int(source['heatingMinTemperature']),
        int(source['heatingMidTemperature'])
    )

def get_default_heating_settings() -> HeatingSettings:
    """Returns default heating settings."""
    return HeatingSettings(
        DEFAULT_MAX_PRICE,
        DEFAULT_MIN_PRICE,
        DEFAULT_HEATING_ENABLED,
        DEFAULT_MAX_TEMPERATURE,
        DEFAULT_MIN_TEMPERATURE,
        DEFAULT_MID_TEMPERATURE
    )
