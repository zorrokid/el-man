from lib.entso_e.entso_e_data_fetcher import EntsoEDataFetcher
from lib.entso_e.entso_e_data_parser import EntsoEDataParser
from models.price import Price

def get_day_ahead_prices(entso_e_token: str, eic_code: str, vat_percentage: int) -> list[Price]:
    data_fetcher = EntsoEDataFetcher(entso_e_token)
    result_str = data_fetcher.get_dayahead_data(eic_code)
    data_parser = EntsoEDataParser(result_str)
    prices = data_parser.parse_dayahead_prices(vat_percentage, 0)
    return prices

