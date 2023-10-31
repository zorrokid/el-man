import time
from typing import List
from lib.adax.models.room import Room
from repositories.firestore_collection_constants import DEVICES_COLLECTION, HOMES_COLLECTION, ROOM_STATE_COLLECTION, ROOMS_COLLECTION

def store_current_room_state(firestore_client, rooms: List[Room]) -> None:
    utc_unix_time = int(time.time())
    for room in rooms:
        firestore_client.collection(ROOMS_COLLECTION).document(str(room.id)).collection(ROOM_STATE_COLLECTION).document(str(utc_unix_time)).set({
            'id': room.id,
            'homeId': room.homeId,
            'timestamp': utc_unix_time,
            'temperature': room.temperature,
            'targetTemperature': room.targetTemperature,
            'heatingEnabled': room.heatingEnabled,
        })
        
def store_homes(firestore_client, home_info):
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

def get_rooms(firestore_client):
    return firestore_client.collection(ROOMS_COLLECTION).stream()