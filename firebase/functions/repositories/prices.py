from firebase_admin import firestore
from datetime import datetime
from models.price import Price
from services.constants import PRICES_COLLECTION

def get_price_for_next_hour(firestore_client) -> (float | None):
    now = datetime.now()
    key = Price.create_price_key(now)
    print(f"Getting price for {key}")
    price_ref = firestore_client.collection(PRICES_COLLECTION).document(key)
    doc = price_ref.get()

    if not doc.exists:
        return None

    price = float(doc.get('price'))
    print(f"Price for {key} is {price}")
    return price
