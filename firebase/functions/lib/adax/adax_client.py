"""Adax API client"""
from datetime import datetime
import sanction
import requests
from lib.adax.models.adax_temperature import AdaxTemperature

from lib.adax.models.api_credentials import ApiCredentials

API_URL = "https://api-1.adax.no/client-api"
TIMEOUT_SECONDS = 10

oauthClinet = sanction.Client(token_endpoint = API_URL + '/auth/token')

class AdaxClient:
    """Adax API client"""
    credentials: ApiCredentials

    def __init__(self, credentials: ApiCredentials):
        self.credentials = credentials

    def get_token(self):
        """Authenticate and obtain JWT token to communicate with Adax API."""
        oauthClinet.request_token(
            grant_type = 'password',
            username = self.credentials.client_id,
            password = self.credentials.credentials
        )
        return oauthClinet.access_token

    def refresh_token(self):
        """Refresh JWT token to communicate with Adax API."""
        oauthClinet.request_token(
            grant_type='refresh_token',
            refresh_token = oauthClinet.refresh_token,
            username = self.credentials.client_id,
            password = self.credentials.credentials
        )
        return oauthClinet.access_token

    def get_headers(self, token):
        """Get headers for authenticated request to Adax API."""
        return { "Authorization": "Bearer " + token }

    def get_api_url(self, path: str) -> str:
        """Get full URL for Adax API endpoint."""
        return API_URL + path

    def set_heating_enabled(self, room_id, enabled: bool, token) -> bool:
        """Enable/disable heating for room."""
        json = { 'rooms': [{ 'id': room_id, 'heatingEnabled': str(enabled) }] }
        api_url = self.get_api_url('/rest/v1/control/')
        headers = self.get_headers(token)
        response = requests.post(api_url, json = json, headers = headers, timeout=TIMEOUT_SECONDS)
        return response.status_code == 200

    def set_room_target_temperature(self, room_id, temperature: AdaxTemperature, token) -> bool:
        """Set target temperature for room."""
        print(f"Setting target temperature for room {room_id} to {temperature}")
        json = { 'rooms': [{
                    'id': room_id, 
                    'targetTemperature': str(temperature.value), 
                    'heatingEnabled': 'true' 
                }]}
        api_url = self.get_api_url('/rest/v1/control/')
        response = requests.post(api_url, json = json, headers = self.get_headers(token), 
                                 timeout=TIMEOUT_SECONDS)
        return response.status_code == 200

    def get_energy_info(self, token, room_id):
        """Get energy info for room."""
        api_url = self.get_api_url('/rest/v1/energy_log/' + str(room_id))
        response = requests.get(api_url, headers = self.get_headers(token), timeout=TIMEOUT_SECONDS)
        json = response.json()
        for log in json['points']:
            from_time = datetime.utcfromtimestamp(int(log['fromTime']) / 1000)
            to_time = datetime.utcfromtimestamp(int(log['toTime']) / 1000)
            energy = log['energyWh']
            print(f"From: {from_time}, To: {to_time}, {energy}")

    def get_home_data(self, token) -> (dict, int):
        """Get home data from Adax API and return it in dict format along with status code."""
        api_url = self.get_api_url('/rest/v1/content/?withEnergy=1')
        response = requests.get(api_url, headers = self.get_headers(token), timeout=TIMEOUT_SECONDS)
        if response.status_code == 200:
            return response.json(), response.status_code
        return None, response.status_code
