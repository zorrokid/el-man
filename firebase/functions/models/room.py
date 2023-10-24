from dataclasses import dataclass

from models.device import Device
from models.device import from_dict as device_from_dict

@dataclass
class Room:
    id: int
    name: str
    heatingEnabled: bool
    temperature: int
    devices: list[Device]

def from_dict(source: dict) -> Room:
    devices = []
    for device in source['devices']:
        devices.append(device_from_dict(device))
    room = Room(source['id'], source['name'], source['heatingEnabled'], source['temperature'], devices)
    return room