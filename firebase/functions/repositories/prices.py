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

def store_prices(prices: list[Price], firestore_client) -> None:
    for price in prices:
        price_key = price.get_price_key()
        docref = firestore_client.collection(PRICES_COLLECTION).document(price_key)
        docref.set({"price" : price.price })
        print(f"Added price {price.price} for {price.get_price_key()}")
