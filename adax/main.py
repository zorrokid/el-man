import os
import sanction
import requests
from datetime import datetime

API_URL = "https://api-1.adax.no/client-api"

oauthClinet = sanction.Client(token_endpoint = API_URL + '/auth/token')

def get_token(credentials: str, account_id: str):
    # Authenticate and obtain JWT token
    oauthClinet.request_token(grant_type = 'password', username = account_id, password = credentials)
    return oauthClinet.access_token

def refresh_token(credentials: str, account_id: str):
    oauthClinet.request_token(grant_type='refresh_token', refresh_token = oauthClinet.refresh_token, username =
    account_id, password = credentials)
    return oauthClinet.access_token

def set_room_target_temperature(roomId, temperature, token):
    # Sets target temperature of the room
    headers = { "Authorization": "Bearer " + token }
    json = { 'rooms': [{ 'id': roomId, 'targetTemperature': str(temperature) }] }
    response = requests.post(API_URL + '/rest/v1/control/', json = json, headers = headers)
    print(response)

def get_energy_info(token, roomId):
    headers = { "Authorization": "Bearer " + token }
    response = requests.get(API_URL + "/rest/v1/energy_log/" + str(roomId), headers = headers)
    json = response.json()
    for log in json['points']:
        fromTime = datetime.utcfromtimestamp(int(log['fromTime']) / 1000)
        toTime = datetime.utcfromtimestamp(int(log['toTime']) / 1000)
        energy = log['energyWh']
        print("From: %15s, To: %15s, %5dwh" % (fromTime, toTime, energy))

def get_homes_info(token):
    headers = { "Authorization": "Bearer " + token }
    response = requests.get(API_URL + "/rest/v1/content/?withEnergy=1", headers = headers)
    print(response)
    json = response.json()
    for room in json['rooms']:
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
    if ('devices' in json):
        for device in json['devices']:
            deviceName = device['name']
            energy = device['energyWh'];
            energyTime = datetime.utcfromtimestamp(int(device['energyTime']) / 1000)
            print("Device: %15s, Time: %15s, Energy: %5dwh, id: %5d" % (deviceName, energyTime, energy, device ['id']))

if __name__ == '__main__':
    credentials = os.environ.get('ADAX_API_CREDENTIALS')
    if (credentials is None):
        print("Please set ADAX_API_CREDENTIALS environment variable")
        exit(1)
    account_id = os.environ.get('ADAX_ACCOUNT_ID')
    if (account_id is None):
        print("Please set ADAX_ACCOUNT_ID environment variable")
        exit(1)
    
    #token = get_token(credentials, account_id)
    token = 'ST.jwX2l7hMced3hAKK2YP5xdDftuhGVgwSw9LFFpLVySwRUpA4Um4TZTy8pGNoinTSMojI5Kxom0S6WOb7dPAenJINO72XoQey9ZPtkASxgDOUMBSTOFFlbFMZVmh0DR1s|133868'
    print(token)
    get_homes_info(token)

