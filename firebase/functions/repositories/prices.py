"""Repository for prices"""
from datetime import datetime, timedelta
from models.price import Price
from repositories.firestore_collection_constants import PRICES_COLLECTION

def get_price_for_next_hour_of(firestore_client, time: datetime) -> (float | None):
    """Gets price for next hour from Firestore database."""
    next_hour = time + timedelta(hours=1)
    key = Price.create_price_key(next_hour)
    price_ref = firestore_client.collection(PRICES_COLLECTION).document(key)
    doc = price_ref.get()

    if not doc.exists:
        return None

    price = float(doc.get('price'))
    return price

def store_prices(prices: list[Price], firestore_client) -> None:
    """Stores prices in Firestore database."""
    for price in prices:
        price_key = price.get_price_key()
        docref = firestore_client.collection(PRICES_COLLECTION).document(price_key)
        docref.set({"price" : price.price })
