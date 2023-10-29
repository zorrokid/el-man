from lib.adax.adax_client import AdaxClient
from lib.adax.models.api_credentials import ApiCredentials
from lib.adax.models.room import Room
from models.heating_settings import HeatingSettings
from datetime import datetime

def set_target_temperatures(rooms: list[Room], price: float, settings: HeatingSettings, adax_api_credentials: ApiCredentials) -> None:
    print("Starting set_heaters")
    
    client = get_client(adax_api_credentials)
    token = client.get_token()

    print(f"Max price  is {settings.maxPrice}")

    for room in rooms:
        print(f"Setting heaters for room {room.id}")
        if price is None or price > settings.maxPrice:
            print(f"Price is not available or or exceed maximum limit {settings.maxPrice}, keeping heating off or turning heating off.")
            if room.heatingEnabled == True: 
                client.set_heating_enabled(room.id, False, token)
        else: 
            newTargetTemperature = settings.heatingMaxTemperature if price < settings.lowPrice else settings.heatingMidTemperature
            print(f"Price {price} is lower than max price {settings.maxPrice}, so turning heating on or keeping heating on. Target temperature is {newTargetTemperature}.")
            if room.targetTemperature != newTargetTemperature:
                client.set_room_target_temperature(room.id, newTargetTemperature * 100, token)

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

def get_client(api_credentials: ApiCredentials) -> AdaxClient:
    return AdaxClient(api_credentials)

def print_home_info(home_info: dict):
    for room in home_info['rooms']:
        roomName = room['name']
        if ('targetTemperature' in room):
            targetTemperature = room['targetTemperature'] / 100.0
        else:
            targetTemperature = 0
        if ('temperature' in room):
            currentTemperature = room['temperature'] / 100.0
        else:
            currentTemperature = 0
        print("Room: %15s, Target: %5.2fC, Temperature: %5.2fC, id: %5d" % (roomName, targetTemperature, currentTemperature, room['id']))
    if ('devices' in home_info):
        for device in home_info['devices']:
            deviceName = device['name']
            energy = device['energyWh'];
            energyTime = datetime.utcfromtimestamp(int(device['energyTime']) / 1000)
            print("Device: %15s, Time: %15s, Energy: %5dwh, id: %5d" % (deviceName, energyTime, energy, device ['id']))