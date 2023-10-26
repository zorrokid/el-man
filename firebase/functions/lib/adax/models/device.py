from dataclasses import dataclass

@dataclass
class Device:
    id: int
    homeId: int
    roomId: int
    name: str
    # unix timestamp
    energyTime: int
    energyWh: int
    type: str

def device_from_dict(source: dict) -> Device:
    return Device(
        source['id'], 
        source['name'], 
        source['energyTime'], 
        source['energyWh'], 
        source['type']
    )