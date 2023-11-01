"""
Heater management module. 
Sets target temperatures for rooms based on day-ahead prices and heating settings.
"""
from datetime import datetime
from firebase_admin import firestore
from domain.target_temperature import calculate_target_temperature
from lib.adax.adax_client import AdaxClient
from lib.adax.models.adax_temperature import AdaxTemperature
from lib.adax.models.api_credentials import ApiCredentials
from lib.adax.models.room import Room, room_from_dict
from models.heating_settings import HeatingSettings
from repositories.heating_settings import get_heating_settings

from repositories.home import store_current_room_state, store_homes
from repositories.prices import get_price_for_next_hour

def set_room_target_temperatures(credentials):
    """Sets target temperatures for rooms based on day-ahead prices and heating settings."""
    home_data = get_home_data(credentials)
    rooms_data = home_data['rooms']
    rooms = []
    for room_data in rooms_data:
        rooms.append(room_from_dict(room_data))

    firestore_client = firestore.client()
    store_current_room_state(firestore_client, rooms)
    heating_settings = get_heating_settings(firestore_client)
    price = get_price_for_next_hour(firestore_client)
    set_target_temperatures(rooms, price, heating_settings, credentials)

def set_target_temperatures(rooms: list[Room], price: float, settings: HeatingSettings,
                            adax_api_credentials: ApiCredentials) -> None:
    """Sets target temperatures using Adax API client."""
    client = get_client(adax_api_credentials)
    token = client.get_token()
    for room in rooms:
        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        if heating_enabled is False and room.heating_enabled is True:
            client.set_heating_enabled(room.id, False, token)
        elif heating_enabled is True and room.target_temperature != target_temperature:
            client.set_room_target_temperature(room.id, AdaxTemperature(target_temperature), token)

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
