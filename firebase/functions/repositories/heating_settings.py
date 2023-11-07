"""Repository module for heating settings"""""
from models.heating_settings import HeatingSettings, get_default_heating_settings
from models.heating_settings import heating_settings_from_dict
from repositories.firestore_collection_constants import HEATING_SETTINGS_COLLECTION

def init_heating_settings(firestore_client, default_settings: HeatingSettings) -> None:
    """Initializes heating settings for all rooms."""
    rooms = firestore_client.collection('rooms').stream()
    heating_settings_ref = firestore_client.collection(HEATING_SETTINGS_COLLECTION)
    for room in rooms:
        settings = heating_settings_ref.document(room.id).get()
        if not settings.exists:
            heating_settings_ref.document(room.id).set(default_settings.to_dict())

def get_heating_settings(firestore_client, room_ids: set[str]) -> dict[str, HeatingSettings]:
    """Gets heating settings from Firestore database by given id's. 
    Returns a map of room id to heating settings."""
    heating_settings_ref = firestore_client.collection(HEATING_SETTINGS_COLLECTION)
    heating_settings_map = {}
    for room_id in room_ids:
        heating_settings = heating_settings_ref.document(room_id).get()
        if not heating_settings.exists:
            print(f"No heating settings found for room {room_id}, using default settings.")
            heating_settings_map[room_id] = get_default_heating_settings()
        else:
            heating_settings_map[room_id] = heating_settings_from_dict(heating_settings.to_dict())
    return heating_settings_map
