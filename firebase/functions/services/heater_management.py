"""
Heater management module. 
Sets target temperatures for rooms based on day-ahead prices and heating settings.
"""
from datetime import datetime
from firebase_admin import firestore
from domain.target_temperature import calculate_target_temperature
from lib.adax.adax_client import AdaxClient
from lib.adax.models.adax_temperature import AdaxTemperature, adax_temperature_from_celcius
from lib.adax.models.api_credentials import ApiCredentials
from lib.adax.models.adax_room import AdaxRoom, adax_room_from_dict
from models.heating_settings import HeatingSettings, get_default_heating_settings
from repositories.heating_settings import get_heating_settings, init_heating_settings

from repositories.home import store_current_room_state, store_homes
from repositories.prices import get_price_for_next_hour_of

def set_room_target_temperatures(credentials):
    """Sets target temperatures for rooms based on day-ahead prices and heating settings."""
    home_data = get_home_data(credentials)
    rooms_data = home_data['rooms']
    rooms = []
    room_ids = set()
    for room_data in rooms_data:
        room = adax_room_from_dict(room_data)
        rooms.append(room)
        room_ids.add(str(room.id))

    firestore_client = firestore.client()
    store_current_room_state(firestore_client, rooms)
    heating_settings = get_heating_settings(firestore_client, room_ids)
    price = get_price_for_next_hour_of(firestore_client, datetime.now())
    set_target_temperatures(rooms, price, heating_settings, credentials)

def set_target_temperatures(rooms: list[AdaxRoom], price: float,
                            heating_settings: dict[str, HeatingSettings],
                            adax_api_credentials: ApiCredentials) -> None:
    """Sets target temperatures using Adax API client."""
    client = get_client(adax_api_credentials)
    token = client.get_token()
    for room in rooms:
        #TODO unify room id's to string
        settings = heating_settings[
            str(room.id)] if str(room.id) in heating_settings else get_default_heating_settings()
        current_temperature = AdaxTemperature(room.temperature).to_celsius()
        (heating_enabled, target_temperature) = calculate_target_temperature(
            price, settings, current_temperature)
        adax_temperature = adax_temperature_from_celcius(target_temperature)
        print(f"Room: {room.name}, Target: {target_temperature}°C, "
              f"Heating enabled: {heating_enabled}.")
        if heating_enabled is False and room.heating_enabled is True:
            print(f"Disabling heating for room {room.name}.")
            client.set_heating_enabled(room.id, False, token)
        elif heating_enabled is True and room.target_temperature != adax_temperature.value:
            prev_target_temp_log_str = f"${AdaxTemperature(room.target_temperature).to_celsius()}°C" if room.target_temperature is not None else "None" 
            print(f"Changing room {room.name} target temperature from "
                  f"{prev_target_temp_log_str} to {target_temperature}°C.")
            client.set_room_target_temperature(room.id, adax_temperature, token)

def set_enabled(rooms, enabled: bool, adax_api_credentials: ApiCredentials) -> None:
    """Sets heating enabled/disabled using Adax API client."""
    client = get_client(adax_api_credentials)
    token = client.get_token()
    for room_doc in rooms:
        room_id = room_doc.get('id')
        client.set_heating_enabled(room_id, enabled, token)

def get_home_data(adax_api_credentials: ApiCredentials) -> dict:
    """Gets home data as dictionary using Adax API client."""
    client = get_client(adax_api_credentials)
    token = client.get_token()
    (home_data, _) = client.get_home_data(token)
    return home_data

def get_and_store_home_data(adax_api_credentials: ApiCredentials) -> None:
    """Gets and stores home data using Adax API client."""
    home_data_json = get_home_data(adax_api_credentials)
    db = firestore.client()
    store_homes(db, home_data_json)

def get_client(api_credentials: ApiCredentials) -> AdaxClient:
    """Create Adax API client."""
    return AdaxClient(api_credentials)

def init_settings() -> None:
    """Initializes heating settings for all rooms missing settings."""
    default_settings = get_default_heating_settings()
    db = firestore.client()
    init_heating_settings(db, default_settings)

def print_home_info(home_info: dict) -> None:
    """Print home info for debugging."""
    for room in home_info['rooms']:
        room_name = room['name']
        if 'targetTemperature' in room:
            target_temperature = AdaxTemperature(room['targetTemperature']).to_celsius()
        else:
            target_temperature = 0
        if 'temperature' in room:
            current_temperature = AdaxTemperature(room['temperature']).to_celsius()
        else:
            current_temperature = 0
        print(f"Room: {room_name}, Target: {target_temperature}C,"
              f" Temperature: {current_temperature}C, id: {room[id]}")
    if 'devices' in home_info:
        for device in home_info['devices']:
            device_name = device['name']
            energy = device['energyWh']
            energy_time = datetime.utcfromtimestamp(int(device['energyTime']) / 1000)
            print(f"Device: {device_name}, Time: {energy_time}, "
                  f"Energy: {energy}, id: {device['id']}")
