import sanction
import requests
from datetime import datetime

API_URL = "https://api-1.adax.no/client-api"

oauthClinet = sanction.Client(token_endpoint = API_URL + '/auth/token')

class AdaxClient:
    def __init__(self, credentials: str, account_id: str):
        self.credentials = credentials
        self.account_id = account_id

    def get_token(self):
        # Authenticate and obtain JWT token
        oauthClinet.request_token(grant_type = 'password', username = self.account_id, password = self.credentials)
        return oauthClinet.access_token

    def refresh_token(self):
        oauthClinet.request_token(
            grant_type='refresh_token', 
            refresh_token = oauthClinet.refresh_token, 
            username = self.account_id, 
            password = self.credentials
        )
        return oauthClinet.access_token

    def get_headers(self, token):
        return { "Authorization": "Bearer " + token }

    def set_heating_enabled(self, roomId, enabled: bool, token) -> bool:
        json = { 'rooms': [{ 'id': roomId, 'heatingEnabled': str(enabled) }] }
        response = requests.post(API_URL + '/rest/v1/control/', json = json, headers = self.get_headers(token))
        print(response)
        return response.status_code == 200

    def set_room_target_temperature(self, roomId, temperature, token) -> bool:
        print(f"Setting target temperature for room {roomId} to {temperature}")
        # Sets target temperature of the room
        json = { 'rooms': [{ 'id': roomId, 'targetTemperature': str(temperature), 'heatingEnabled': 'true' }] }
        response = requests.post(API_URL + '/rest/v1/control/', json = json, headers = self.get_headers(token))
        print(response)
        return response.status_code == 200

    def get_energy_info(self, token, roomId):
        response = requests.get(API_URL + "/rest/v1/energy_log/" + str(roomId), headers = self.get_headers(token))
        json = response.json()
        for log in json['points']:
            fromTime = datetime.utcfromtimestamp(int(log['fromTime']) / 1000)
            toTime = datetime.utcfromtimestamp(int(log['toTime']) / 1000)
            energy = log['energyWh']
            print("From: %15s, To: %15s, %5dwh" % (fromTime, toTime, energy))

    def get_house_info(self, token) -> (dict, int):
        response = requests.get(API_URL + "/rest/v1/content/?withEnergy=1", headers = self.get_headers(token))
        if (response.status_code == 200):
            return response.json(), response.status_code
        return None, response.status_code
