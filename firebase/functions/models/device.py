from dataclasses import dataclass

@dataclass
class Device:
    id: int
    name: str
    energyTime: int
    energyWh: int
    type: str

def from_dict(source: dict) -> Device:
    device = Device(source['id'], source['name'], source['energyTime'], source['energyWh'], source['type'])
    return device