from firebase_functions import https_fn, scheduler_fn
from firebase_functions.params import StringParam, IntParam, SecretParam
from firebase_admin import initialize_app, firestore

from lib.entso_e.entso_e_data_fetcher import EntsoEDataFetcher
from lib.entso_e.entso_e_data_parser import EntsoEDataParser


ENTSO_E_TOKEN = SecretParam("ENTSO_E_TOKEN")
EIC_CODE = StringParam('EIC_CODE') # '10YFI-1--------U'
VAT_PERCENTAGE = IntParam("VAT_PERCENTAGE") # 24
UTC_DIFF = IntParam("UTC_DIFF") # 3

initialize_app()
@scheduler_fn.on_schedule(schedule="every day 19:40", region="europe-central2", secrets=[ENTSO_E_TOKEN])
def fetch_day_ahead_prices(req: https_fn.Request) -> None:
    print("Fetching day ahead prices...")
    data_fetcher = EntsoEDataFetcher(ENTSO_E_TOKEN.value)
    result_str = data_fetcher.get_dayahead_data(EIC_CODE.value)
    data_parser = EntsoEDataParser(result_str)
    prices = data_parser.parse_dayahead_prices(VAT_PERCENTAGE.value, 0)
    db = firestore.client()
    for price in prices:
        docref = db.collection('DayAheadPrices').document(price.get_price_key())
        docref.set({"price" : price.price })
        print(f"Added price {price.price} for {price.get_price_key()}")

    print("Finished fetching day ahead prices...")

