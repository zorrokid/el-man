# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import scheduler_fn
from firebase_functions.params import StringParam, IntParam
from firebase_admin import initialize_app, firestore

from lib.entso_e.entso_e_data_fetcher import EntsoEDataFetcher
from lib.entso_e.entso_e_data_parser import EntsoEDataParser

initialize_app()

ENTSO_E_TOKEN = StringParam("ENTSO_E_TOKEN")
EIC_CODE = StringParam('EIC_CODE') # '10YFI-1--------U'
VAT_PERCENTAGE = IntParam("VAT_PERCENTAGE") # 24
UTC_DIFF = IntParam("UTC_DIFF") # 3

@scheduler_fn.on_schedule(schedule="every day 00:00")
def fetch_day_ahead_prices(event: scheduler_fn.ScheduledEvent) -> None:
    print("Fetching day ahead prices...")
    data_fetcher = EntsoEDataFetcher(ENTSO_E_TOKEN.get())
    result_str = data_fetcher.get_dayahead_data(EIC_CODE.get())
    data_parser = EntsoEDataParser(result_str)
    prices = data_parser.parse_dayahead_prices(VAT_PERCENTAGE.get(), 0)
    db = firestore.client()
    prices_collection_ref = db.collection('DayAheadPrices')
    for price in prices:
        prices_collection_ref.document(price.get_price_key()).set(price.value)

