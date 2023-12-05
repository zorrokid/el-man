"""This module contains the logic to fetch and store day ahead prices"""""
from firebase_admin import firestore
from lib.entso_e.entso_e_data_fetcher import EntsoEDataFetcher
from lib.entso_e.entso_e_data_parser import EntsoEDataParser
from models.price import Price
from repositories.prices import store_prices

def fetch_and_store_day_ahead_prices(entso_e_token, eic_code, vat_percentage):
    """Fetches and stores day ahead prices."""
    prices = get_day_ahead_prices(entso_e_token, eic_code, vat_percentage)
    if not prices:
        print("No prices fetched")
        return
    store_prices(prices, firestore.client())

def get_day_ahead_prices(entso_e_token: str, eic_code: str, vat_percentage: int) -> list[Price]:
    """Gets day ahead prices."""
    data_fetcher = EntsoEDataFetcher(entso_e_token)
    result_str = data_fetcher.get_dayahead_data(eic_code)
    data_parser = EntsoEDataParser(result_str)
    prices = data_parser.parse_dayahead_prices(vat_percentage, 0)
    return prices
