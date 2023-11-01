from firebase_admin import firestore
from domain.target_temperature import calculate_target_temperature
from lib.adax.adax_client import AdaxClient
from lib.adax.models.adax_temperature import AdaxTemperature
from lib.adax.models.api_credentials import ApiCredentials
from lib.adax.models.room import Room, room_from_dict
from models.heating_settings import HeatingSettings
from datetime import datetime

from repositories.home import get_heating_settings, store_current_room_state, store_homes
from repositories.prices import get_price_for_next_hour

def set_room_target_temperatures(credentials):
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

def set_target_temperatures(rooms: list[Room], price: float, settings: HeatingSettings, adax_api_credentials: ApiCredentials) -> None:
    client = get_client(adax_api_credentials)
    token = client.get_token()
    for room in rooms:
        (heatingEnabled, targetTemperature) = calculate_target_temperature(price, settings)
        if heatingEnabled == False and room.heatingEnabled == True:
            client.set_heating_enabled(room.id, False, token)
        elif heatingEnabled == True and room.targetTemperature != targetTemperature: 
            client.set_room_target_temperature(room.id, AdaxTemperature(targetTemperature), token)

def set_enabled(rooms, enabled: bool, adax_api_credentials: ApiCredentials) -> None:
    client = get_client(adax_api_credentials)
    token = client.get_token()
    for roomDoc in rooms:
        roomId = roomDoc.get('id')
        client.set_heating_enabled(roomId, enabled, token)

def get_home_data(adax_api_credentials: ApiCredentials):
    client = get_client(adax_api_credentials) 
    token = client.get_token()
    (home_data, _) = client.get_home_data(token)
    return home_data

def get_and_store_home_data(adax_api_credentials: ApiCredentials):
    home_data_json = get_home_data(adax_api_credentials) 
    db = firestore.client()
    store_homes(db, home_data_json)

def get_client(api_credentials: ApiCredentials) -> AdaxClient:
    return AdaxClient(api_credentials)

def print_home_info(home_info: dict):
    for room in home_info['rooms']:
        roomName = room['name']
        if ('targetTemperature' in room):
            targetTemperature = AdaxTemperature(room['targetTemperature']).to_celsius()
        else:
            targetTemperature = 0
        if ('temperature' in room):
            currentTemperature = AdaxTemperature(room['temperature']).to_celsius()
        else:
            currentTemperature = 0
        print("Room: %15s, Target: %5.2fC, Temperature: %5.2fC, id: %5d" % (roomName, targetTemperature, currentTemperature, room['id']))
    if ('devices' in home_info):
        for device in home_info['devices']:
            deviceName = device['name']
            energy = device['energyWh']
            energyTime = datetime.utcfromtimestamp(int(device['energyTime']) / 1000)
            print("Device: %15s, Time: %15s, Energy: %5dwh, id: %5d" % (deviceName, energyTime, energy, device ['id']))
