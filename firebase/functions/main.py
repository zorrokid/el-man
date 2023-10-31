import json
from firebase_functions import https_fn, scheduler_fn
from firebase_functions.params import StringParam, IntParam, SecretParam
from firebase_admin import initialize_app, firestore
from lib.adax.models.api_credentials import ApiCredentials
from lib.adax.models.room import room_from_dict

from repositories.prices import get_price_for_next_hour, store_prices
from services.day_ahead_prices import get_day_ahead_prices

from services.heater_management import get_home_data, set_enabled, set_target_temperatures
from repositories.home_repository import get_heating_settings, get_rooms, store_current_room_state, store_homes

ENTSO_E_TOKEN = SecretParam("ENTSO_E_TOKEN")
EIC_CODE = StringParam('EIC_CODE') # '10YFI-1--------U'
VAT_PERCENTAGE = IntParam("VAT_PERCENTAGE") # 24
UTC_DIFF = IntParam("UTC_DIFF") # 3

ADAX_API_CREDENTIALS = SecretParam("ADAX_API_CREDENTIALS")
ADAX_CLIENT_ID = SecretParam("ADAX_CLIENT_ID")

FETCH_DAYAHEAD_PRICES_SCHEDULE = "every day 19:40"
SET_TARGET_TEMPERATURES_SCHEDULE = "58 * * * *"

initialize_app()

@scheduler_fn.on_schedule(schedule=FETCH_DAYAHEAD_PRICES_SCHEDULE, region="europe-central2", secrets=[ENTSO_E_TOKEN])
def fetch_day_ahead_prices(req: https_fn.Request) -> None:
    _fetch_day_ahead_prices(ENTSO_E_TOKEN.value, EIC_CODE.value, VAT_PERCENTAGE.value)

# https trigger for local emulator testing purposes
@https_fn.on_request(region="europe-central2", secrets=[ADAX_API_CREDENTIALS, ADAX_CLIENT_ID])
def fetch_day_ahead_prices_http(req: https_fn.Request) -> https_fn.Response:
    _fetch_day_ahead_prices(ENTSO_E_TOKEN.value, EIC_CODE.value, VAT_PERCENTAGE.value) 
    return https_fn.Response("OK") 

def _fetch_day_ahead_prices(entso_e_token, eic_code, vat_percentage):
    prices = get_day_ahead_prices(entso_e_token, eic_code, vat_percentage)
    store_prices(prices, firestore.client())

@scheduler_fn.on_schedule(schedule=SET_TARGET_TEMPERATURES_SCHEDULE, region="europe-central2", secrets=[ADAX_API_CREDENTIALS, ADAX_CLIENT_ID])
def set_temperatures(req: https_fn.Request) -> None:
    _set_temperatures(ApiCredentials(ADAX_API_CREDENTIALS.value, ADAX_CLIENT_ID.value))

# https trigger for local emulator testing purposes
@https_fn.on_request(region="europe-central2", secrets=[ADAX_API_CREDENTIALS, ADAX_CLIENT_ID])
def set_temperatures_http(req: https_fn.Request) -> https_fn.Response:
    _set_temperatures(ApiCredentials(ADAX_API_CREDENTIALS.value, ADAX_CLIENT_ID.value))
    return https_fn.Response("OK") 

def _set_temperatures(credentials):
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

@https_fn.on_request(region="europe-central2", secrets=[ADAX_API_CREDENTIALS, ADAX_CLIENT_ID])
def set_heating_enabled(req: https_fn.Request) -> https_fn.Response:
    enabled = req.args.get('enabled') == 'true'
    house_id = req.args.get('house_id')
    if house_id is None:
        return https_fn.Response("Missing house_id", 400)
    rooms = get_rooms(firestore.client(), house_id)
    set_enabled(rooms, enabled, ApiCredentials(ADAX_API_CREDENTIALS.value, ADAX_CLIENT_ID.value))
    return https_fn.Response("OK")

@https_fn.on_request(region="europe-central2", secrets=[ADAX_API_CREDENTIALS, ADAX_CLIENT_ID])
def get_house_info(req: https_fn.Request) -> https_fn.Response:
    home_data_json = get_home_data(ApiCredentials(ADAX_API_CREDENTIALS.value, ADAX_CLIENT_ID.value)) 
    # homes = parse_homes(home_data_json)
    # rooms = parse_rooms(home_data_json)
    # devices = parse_devices(home_data_json)
    db = firestore.client()
    store_homes(db, home_data_json)
    return https_fn.Response(json.dumps(home_data_json))