import time
from typing import List
from lib.adax.models.room import Room
from models.heating_settings import HeatingSettings, get_default_heating_settings, heating_settings_from_dict
from services.constants import DEVICES_COLLECTION, HEATING_SETTINGS_COLLECTION, HOMES_COLLECTION, ROOM_STATE_COLLECTION, ROOMS_COLLECTION

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

def init_heating_settings(firestore_client) -> None:
    homes = firestore_client.collection(HOMES_COLLECTION).stream() 
    default_settings = get_default_heating_settings()
    for home in homes:
        settings = firestore_client.collection(HEATING_SETTINGS_COLLECTION).document(home.id).get()
        if not settings.exists:
            firestore_client.collection(HEATING_SETTINGS_COLLECTION).document(home.id).set(default_settings.to_dict())

def get_heating_settings(firestore_client) -> HeatingSettings:
    # expect only one document currently
    heating_settings = next(firestore_client.collection(HEATING_SETTINGS_COLLECTION).stream(), None)
    if heating_settings is None:
        print("No heating settings found, using default settings")
        return get_default_heating_settings()
    return heating_settings_from_dict(heating_settings.to_dict())

def get_rooms(firestore_client):
    return firestore_client.collection(ROOMS_COLLECTION).stream()