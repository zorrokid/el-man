import os
import sys
from entso_e.entso_e_data_parser import EntsoEDataParser
from entso_e.entso_e_data_fetcher import EntsoEDataFetcher
from util.arg_parser import ArgParser
from util.price_processor import PriceProcessor

def get_local_data():
    return open('./example_data/example_result.xml', 'r').read()

def get_online_data(token, eic_code):
    return EntsoEDataFetcher(token).get_dayahead_data(eic_code)

if __name__ == '__main__':
    token = os.environ.get('TOKEN')
    if (token is None):
        print("Please set TOKEN environment variable")
        exit(1)

    eic_code, utc_diff, vat_percentage, use_local_data = ArgParser(sys.argv).parse()

    if use_local_data:
        data = get_local_data() 
    else:
        data = get_online_data(token, eic_code)

    prices = EntsoEDataParser(data).parse_dayahead_prices(vat_percentage, utc_diff)
    price_processor = PriceProcessor(prices).print()