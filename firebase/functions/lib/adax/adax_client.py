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

    def set_room_target_temperature(self, roomId, temperature, token):
        # Sets target temperature of the room
        headers = { "Authorization": "Bearer " + token }
        json = { 'rooms': [{ 'id': roomId, 'targetTemperature': str(temperature) }] }
        response = requests.post(API_URL + '/rest/v1/control/', json = json, headers = headers)
        print(response)

    def get_energy_info(self, token, roomId):
        headers = { "Authorization": "Bearer " + token }
        response = requests.get(API_URL + "/rest/v1/energy_log/" + str(roomId), headers = headers)
        json = response.json()
        for log in json['points']:
            fromTime = datetime.utcfromtimestamp(int(log['fromTime']) / 1000)
            toTime = datetime.utcfromtimestamp(int(log['toTime']) / 1000)
            energy = log['energyWh']
            print("From: %15s, To: %15s, %5dwh" % (fromTime, toTime, energy))

    def get_house_info(self, token) -> (dict, int):
        headers = { "Authorization": "Bearer " + token }
        response = requests.get(API_URL + "/rest/v1/content/?withEnergy=1", headers = headers)
        if (response.status_code == 200):
            return response.json(), response.status_code
        return None, response.status_code
