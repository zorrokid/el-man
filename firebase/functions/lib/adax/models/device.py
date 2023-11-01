"""Model for device in Adax API."""
from dataclasses import dataclass

@dataclass
class Device:
    """Represents Adax device."""
    id: int
    home_id: int
    room_id: int
    name: str
    # unix timestamp
    energy_time: int
    energy_wh: int
    type: str

def device_from_dict(source: dict) -> Device:
    """Converts dictionary to Device."""
    return Device(
        source['id'],
        source['homeId'],
        source['roomId'],
        source['name'],
        source['energyTime'],
        source['energyWh'],
        source['type']
    )
