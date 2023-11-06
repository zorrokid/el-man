"""Repository module for heating settings"""""
from models.heating_settings import HeatingSettings, get_default_heating_settings
from models.heating_settings import heating_settings_from_dict
from repositories.firestore_collection_constants import HEATING_SETTINGS_COLLECTION
from repositories.firestore_collection_constants import HOMES_COLLECTION

def init_heating_settings(firestore_client) -> None:
    """Initializes heating settings for all homes."""
    homes = firestore_client.collection(HOMES_COLLECTION).stream()
    default_settings = get_default_heating_settings()
    for home in homes:
        settings = firestore_client.collection(HEATING_SETTINGS_COLLECTION).document(home.id).get()
        if not settings.exists:
            firestore_client.collection(HEATING_SETTINGS_COLLECTION).document(
                home.id).set(default_settings.to_dict())

def get_heating_settings(firestore_client, setting_ids: set) -> dict[str, HeatingSettings]:
    """Gets heating settings from Firestore database by given id's. 
    Returns a map of id to heating settings."""
    heating_settings_ref = firestore_client.collection(HEATING_SETTINGS_COLLECTION)
    heating_setttings_map = {}
    for setting_id in setting_ids:
        heating_settings = heating_settings_ref.document(setting_id).get()
        if heating_settings is None:
            print("No heating settings found, using default settings")
            heating_settings[setting_id] = get_default_heating_settings()
        else:
            heating_settings[setting_id] = heating_settings_from_dict(heating_settings)
    return heating_setttings_map
