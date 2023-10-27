from dataclasses import dataclass

@dataclass
class HeatingSettings:
    maxPrice: int
    lowPrice: int
    heatingEnabled: bool 
    heatingMaxTemperature: int
    heatingMinTemperature: int
    heatingMidTemperature: int

    def to_dict(self):
        return {
            'maxPrice': self.maxPrice,
            'lowPrice': self.lowPrice,
            'heatingEnabled': self.heatingEnabled,
            'heatingMaxTemperature': self.heatingMaxTemperature,
            'heatingMinTemperature': self.heatingMinTemperature,
            'heatingMidTemperature': self.heatingMidTemperature
        }

def heating_settings_from_dict(source: dict) -> HeatingSettings:
    return HeatingSettings(
        int(source['maxPrice']), 
        int(source['lowPrice']), 
        bool(source['heatingEnabled']), 
        int(source['heatingMaxTemperature']), 
        int(source['heatingMinTemperature']), 
        int(source['heatingMidTemperature'])
    )

def get_default_heating_settings() -> HeatingSettings:
    return HeatingSettings(5, 2, True, 20, 5, 10)