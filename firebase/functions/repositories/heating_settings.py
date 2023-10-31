from models.heating_settings import HeatingSettings, get_default_heating_settings, heating_settings_from_dict
from repositories.firestore_collection_constants import HEATING_SETTINGS_COLLECTION, HOMES_COLLECTION

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
