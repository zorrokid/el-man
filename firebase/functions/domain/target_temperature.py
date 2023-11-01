"""This module contains the logic for calculating the target temperature based on the current price and the heating settings."""""
from models.heating_settings import HeatingSettings

def calculate_target_temperature(price: float, settings: HeatingSettings) -> (bool, int):
    """Calculates the target temperature based on the current price and the heating settings."""
    if price is None or price > settings.max_price or settings.heating_enabled is False:
        return (False, 0)
    else:
        target_temperature = settings.heating_max_temperature if price < settings.low_price else settings.heating_mid_temperature
        return (True, target_temperature)
