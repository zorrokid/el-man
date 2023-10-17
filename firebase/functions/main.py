from firebase_functions import https_fn
from firebase_functions.params import StringParam, IntParam, SecretParam
from firebase_admin import initialize_app, firestore

from lib.entso_e.entso_e_data_fetcher import EntsoEDataFetcher
from lib.entso_e.entso_e_data_parser import EntsoEDataParser


token = SecretParam("ENTSO_E_TOKEN")
eic_code = StringParam('EIC_CODE') # '10YFI-1--------U'
vat_percentage = IntParam("VAT_PERCENTAGE") # 24
utc_diff = IntParam("UTC_DIFF") # 3

initialize_app()
#@scheduler_fn.on_schedule(schedule="every day 00:00")
@https_fn.on_request()
def fetch_day_ahead_prices(req: https_fn.Request) -> https_fn.Response:
    print("Fetching day ahead prices...")
    data_fetcher = EntsoEDataFetcher(token.value)
    result_str = data_fetcher.get_dayahead_data(eic_code.value)
    data_parser = EntsoEDataParser(result_str)
    prices = data_parser.parse_dayahead_prices(vat_percentage.value, 0)
    db = firestore.client()
    for price in prices:
        docref = db.collection('DayAheadPrices').document(price.get_price_key())
        docref.set({"price" : price.price })
        print(f"Added price {price.price} for {price.get_price_key()}")

    print("Finished fetching day ahead prices...")
    return https_fn.Response("Finished fetching day ahead prices.")

