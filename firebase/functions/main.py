from firebase_functions import https_fn, scheduler_fn
from firebase_functions.params import StringParam, IntParam, SecretParam
from firebase_admin import initialize_app
from lib.adax.models.api_credentials import ApiCredentials
from services.day_ahead_prices import fetch_and_store_day_ahead_prices
from services.heater_management import get_and_store_home_data, set_room_target_temperatures

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
    fetch_and_store_day_ahead_prices(ENTSO_E_TOKEN.value, EIC_CODE.value, VAT_PERCENTAGE.value)

@scheduler_fn.on_schedule(schedule=SET_TARGET_TEMPERATURES_SCHEDULE, region="europe-central2", secrets=[ADAX_API_CREDENTIALS, ADAX_CLIENT_ID])
def set_temperatures(req: https_fn.Request) -> None:
    set_room_target_temperatures(ApiCredentials(ADAX_API_CREDENTIALS.value, ADAX_CLIENT_ID.value))

# https triggers for local emulator testing purposes

@https_fn.on_request(region="europe-central2", secrets=[ADAX_API_CREDENTIALS, ADAX_CLIENT_ID])
def fetch_day_ahead_prices_http(req: https_fn.Request) -> https_fn.Response:
    fetch_and_store_day_ahead_prices(ENTSO_E_TOKEN.value, EIC_CODE.value, VAT_PERCENTAGE.value) 
    return https_fn.Response("OK") 

@https_fn.on_request(region="europe-central2", secrets=[ADAX_API_CREDENTIALS, ADAX_CLIENT_ID])
def set_temperatures_http(req: https_fn.Request) -> https_fn.Response:
    set_room_target_temperatures(ApiCredentials(ADAX_API_CREDENTIALS.value, ADAX_CLIENT_ID.value))
    return https_fn.Response("OK") 

@https_fn.on_request(region="europe-central2", secrets=[ADAX_API_CREDENTIALS, ADAX_CLIENT_ID])
def get_house_info(req: https_fn.Request) -> https_fn.Response:
    get_and_store_home_data(ApiCredentials(ADAX_API_CREDENTIALS.value, ADAX_CLIENT_ID.value))
    return https_fn.Response("OK")