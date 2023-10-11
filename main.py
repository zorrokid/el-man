import os
import sys
from entso_e.entso_e_data_parser import EntsoEDataParser
from entso_e.entso_e_data_fetcher import EntsoEDataFetcher
from arg_parser import ArgParser
from price_processor import PriceProcessor

def get_local_data():
    data = open('./example_data/example_result.xml', 'r').read()
    return data

def get_online_data(token, eic_code):
    data_fetcher = EntsoEDataFetcher(token)
    return data_fetcher.get_data(eic_code)

def print_prices(prices):
    for price in prices:
        print("Time: ", price.time)
        print("Price: {0} c/kWh".format(price.price))

if __name__ == '__main__':
    token = os.environ.get('TOKEN')
    if (token is None):
        print("Please set TOKEN environment variable")
        exit(1)

    arg_parser = ArgParser(sys.argv)
    eic_code, utc_diff, vat_percentage, use_local_data = arg_parser.parse()

    if use_local_data:
        data = get_local_data() 
    else:
        data = get_online_data(token, eic_code)

    parser = EntsoEDataParser(data)
    prices = parser.parse_data(vat_percentage, utc_diff)
    price_processor = PriceProcessor(prices)
    price_processor.process()