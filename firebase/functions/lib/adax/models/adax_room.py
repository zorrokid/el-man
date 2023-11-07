"""Models for Adax API room."""
from dataclasses import dataclass

@dataclass
class AdaxRoom:
    """Represents room in Adax API."""
    id: int
    home_id: int
    name: str
    heating_enabled: bool
    temperature: int
    target_temperature: int | None

def adax_room_from_dict(source: dict) -> AdaxRoom:
    """Converts dictionary to Room."""
    return AdaxRoom(
        source['id'],
        source['homeId'],
        source['name'],
        source['heatingEnabled'],
        source['temperature'],
        source['targetTemperature'] if 'targetTemperature' in source else None,
    )
