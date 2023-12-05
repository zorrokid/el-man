"""This module contains the logic for calculating the target temperature 
based on the current price and the heating settings."""
from models.heating_settings import HeatingSettings

def calculate_target_temperature(
        price: float,
        settings: HeatingSettings,
        current_temperature: int) -> (bool, int):

    """Calculates the target temperature based on the current price and the heating settings."""
    if settings.heating_enabled is False:
        return (False, 0)

    if (price is None or price > settings.max_price) and current_temperature > settings.heating_min_temperature:
        return (False, 0)

    if (price is None or price > settings.max_price) and current_temperature <= settings.heating_min_temperature:
        return (True, settings.heating_min_temperature)

    target_temperature = settings.heating_max_temperature if price < settings.low_price else settings.heating_mid_temperature
    return (True, target_temperature)
