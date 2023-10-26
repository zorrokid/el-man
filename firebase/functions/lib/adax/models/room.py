from dataclasses import dataclass

@dataclass
class Room:
    id: int
    homeId: int
    name: str
    heatingEnabled: bool
    temperature: int
    targetTemperature: int | None

def room_from_dict(source: dict) -> Room:
    return Room(
        source['id'], 
        source['name'], 
        source['heatingEnabled'], 
        source['temperature'], 
        source['targetTemperature'] if 'targetTemperature' in source else None
    )