"""Models for room. Different from original Adax API models because of heating settings id."""
from dataclasses import dataclass

@dataclass
class Room:
    """Represents room in Adax API. Also includes heating settings id for the room."""
    id: int
    home_id: int
    name: str
    heating_enabled: bool
    temperature: int
    target_temperature: int | None
    heating_settings_id: str | None

def room_from_dict(source: dict) -> Room:
    """Converts dictionary to Room."""
    return Room(
        source['id'],
        source['homeId'],
        source['name'],
        source['heatingEnabled'],
        source['temperature'],
        source['targetTemperature'] if 'targetTemperature' in source else None,
        source['heatingSettingsId'] if 'heatingSettingsId' in source else None
    )
