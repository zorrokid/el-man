import json
from firebase_functions import https_fn, scheduler_fn
from firebase_functions.params import StringParam, IntParam, SecretParam
from firebase_admin import initialize_app, firestore
from lib.adax.adax_client import AdaxClient

from lib.entso_e.entso_e_data_fetcher import EntsoEDataFetcher
from lib.entso_e.entso_e_data_parser import EntsoEDataParser

from datetime import datetime

from lib.entso_e.models.price import Price


ENTSO_E_TOKEN = SecretParam("ENTSO_E_TOKEN")
EIC_CODE = StringParam('EIC_CODE') # '10YFI-1--------U'
VAT_PERCENTAGE = IntParam("VAT_PERCENTAGE") # 24
UTC_DIFF = IntParam("UTC_DIFF") # 3

ADAX_API_CREDENTIALS = SecretParam("ADAX_API_CREDENTIALS")
ADAX_CLIENT_ID = StringParam("ADAX_CLIENT_ID")

PRICES_COLLECTION = "DayAheadPrices"

DAYAHEAD_PRICE_FETCH_SCHDULE = "every day 19:40"

@scheduler_fn.on_schedule(schedule=DAYAHEAD_PRICE_FETCH_SCHDULE, region="europe-central2", secrets=[ENTSO_E_TOKEN])
def fetch_day_ahead_prices(req: https_fn.Request) -> None:
    print("Fetching day ahead prices...")
    data_fetcher = EntsoEDataFetcher(ENTSO_E_TOKEN.value)
    result_str = data_fetcher.get_dayahead_data(EIC_CODE.value)
    data_parser = EntsoEDataParser(result_str)
    prices = data_parser.parse_dayahead_prices(VAT_PERCENTAGE.value, 0)
    db = firestore.client()
    for price in prices:
        docref = db.collection(PRICES_COLLECTION).document(price.get_price_key())
        docref.set({"price" : price.price })
        print(f"Added price {price.price} for {price.get_price_key()}")

    print("Finished fetching day ahead prices...")

EVERY_HOUR = "0 * * * *"

@scheduler_fn.on_schedule(schedule=EVERY_HOUR, region="europe-central2", secrets=[ADAX_API_CREDENTIALS, ADAX_CLIENT_ID])
def set_heaters(req: https_fn.Request) -> None:
    print("Starting set_heaters")
    now = datetime.datetime.now()
    key = Price.create_price_key(now)
    db = firestore.client()
    price_ref = db.collection(PRICES_COLLECTION).document(key)
    doc = price_ref.get()

    if doc.exists:
        price = float(doc.to_dict()['price'])
        print(f"Price for {key} is {price} ")

    print("Finished set_heaters")

@https_fn.on_request(region="europe-central2", secrets=[ADAX_API_CREDENTIALS, ADAX_CLIENT_ID])
def get_house_info(req: https_fn.Request) -> https_fn.Response:
    client = AdaxClient(ADAX_API_CREDENTIALS.value, ADAX_CLIENT_ID.value)
    token = client.get_token()

    (house_info, status_code) = client.get_house_info(token)
    if status_code != 200:
        return https_fn.Response("Error getting house info", status_code)

    print_house_info(house_info)
    return https_fn.Response(json.dumps(house_info))

def print_house_info(house_info: dict):
    for room in house_info['rooms']:
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
    if ('devices' in house_info):
        for device in house_info['devices']:
            deviceName = device['name']
            energy = device['energyWh'];
            energyTime = datetime.utcfromtimestamp(int(device['energyTime']) / 1000)
            print("Device: %15s, Time: %15s, Energy: %5dwh, id: %5d" % (deviceName, energyTime, energy, device ['id']))

    return https_fn.Response("OK")

def get_target_temperature(price: float):
    current_temperature = 10 # get current temperature
    get_target_temperature = 15 # get target temperature

    new_temperature = current_temperature # calculate baed on current temperature and price for next few hours
    # for example: 
    # if price for next few hours is low, increase temperature gradually
    # if price is low for next hour but rises after that then increase temperature high for next hour
    # if price for next few hours is high, decrease temperature fast
    # if price exceeds some threshold, turn off heating