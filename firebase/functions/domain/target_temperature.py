from models.heating_settings import HeatingSettings

def calculate_target_temperature(price: float, settings: HeatingSettings) -> (bool, int):
    if price is None or price > settings.maxPrice or settings.heatingEnabled == False:
        return (False, 0)
    else: 
        newTargetTemperature = settings.heatingMaxTemperature if price < settings.lowPrice else settings.heatingMidTemperature
        return (True, newTargetTemperature)

