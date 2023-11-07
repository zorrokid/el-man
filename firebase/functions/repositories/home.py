"""Home repository module."""
import time
from typing import List
from lib.adax.models.adax_room import AdaxRoom
from models.room import room_from_dict
from repositories.firestore_collection_constants import DEVICES_COLLECTION
from repositories.firestore_collection_constants import HOMES_COLLECTION
from repositories.firestore_collection_constants import ROOM_STATE_COLLECTION
from repositories.firestore_collection_constants import ROOMS_COLLECTION

def store_current_room_state(firestore_client, rooms: List[AdaxRoom]) -> None:
    """Stores current room state in Firestore database."""
    utc_unix_time = int(time.time())
    for room in rooms:
        firestore_client.collection(ROOMS_COLLECTION).document(
            str(room.id)).collection(ROOM_STATE_COLLECTION).document(str(utc_unix_time)).set({
            'id': room.id,
            'homeId': room.home_id,
            'timestamp': utc_unix_time,
            'temperature': room.temperature,
            'targetTemperature': room.target_temperature,
            'heatingEnabled': room.heating_enabled,
        })

def store_homes(firestore_client, home_info):
    """Stores home info in Firestore database."""
    homes = home_info['homes']
    homes_collection_ref = firestore_client.collection(HOMES_COLLECTION)
    for home in homes:
        homes_collection_ref.document(str(home['id'])).set(home)

    rooms_collection_ref = firestore_client.collection(ROOMS_COLLECTION)
    rooms = home_info['rooms']
    for room in rooms:
        rooms_collection_ref.document(str(room['id'])).set(room)

    devices_collection_ref = firestore_client.collection(DEVICES_COLLECTION)
    devices = home_info['devices']
    for device in devices:
        devices_collection_ref.document(str(device['id'])).set(device)

def get_rooms(firestore_client) -> dict[str, AdaxRoom]:
    """Gets rooms from Firestore database and returns a map of id to room."""
    rooms = {}
    rooms_stream = firestore_client.collection(ROOMS_COLLECTION).stream()
    for room in rooms_stream:
        rooms[room.id] = room_from_dict(room.to_dict())
    return rooms
