"""This module contains the logic for calculating the target temperature 
based on the current price and the heating settings."""
from models.heating_settings import HeatingSettings

def calculate_target_temperature(
        price: float,
        settings: HeatingSettings,
        current_temperature_in_celcius: int) -> (bool, int):

    """Calculates the target temperature based on the current price and the heating settings."""

    if (price is None or price > settings.max_price) and current_temperature_in_celcius > settings.heating_min_temperature:
        return (False, settings.heating_min_temperature)

    if (price is None or price > settings.max_price) and current_temperature_in_celcius <= settings.heating_min_temperature:
        return (True, settings.heating_min_temperature)

    target_temperature = settings.heating_max_temperature if price < settings.low_price else settings.heating_mid_temperature
    return (True, target_temperature)
