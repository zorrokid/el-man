from dataclasses import dataclass

from models.room import Room
from models.room import from_dict as room_from_dict

@dataclass
class Home:
    id: str
    name: str
    price_max: int | None 
    rooms: list[Room]

def from_dict(source: dict) -> Home:
    rooms = []
    for room in source['rooms']:
        rooms.append(room_from_dict(room))
    home = Home(source['id'], source['name'], source['price_max'], rooms)
    return home 
