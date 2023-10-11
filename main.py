import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from entso_e.entso_e_data_parser import EntsoEDataParser
from entso_e.entso_e_data_fetcher import EntsoEDataFetcher

TOKEN = os.environ.get('TOKEN')

EIC_CODE = '10YFI-1--------U'

def get_local_data():
    tree = ET.parse('./example_data/example_result.xml')
    root = tree.getroot()
    return root

def get_online_data(eic_code):
    date_from = datetime.now()
    date_to = date_from + timedelta(days=1)
    data_fetcher = EntsoEDataFetcher(TOKEN)
    return data_fetcher.get_data(date_from, date_to, eic_code)

def print_prices(prices):
    for price in prices:
        print("Time: ", price.time)
        print("Price: {0} c/kWh".format(price.price))

if __name__ == '__main__':
    if (TOKEN is None):
        print("Please set TOKEN environment variable")
        exit(1)

    # read command line argument for Domain EIC Code
    if len(sys.argv) > 1:
       eic_code = sys.argv[1]
    else:
        eic_code = EIC_CODE

    # read command line argument for difference from UTC in hours
    if (len(sys.argv) > 2):
        utc_diff = int(sys.argv[2])
    else:
        utc_diff = 3

    # read vat percentage from command line argument
    if (len(sys.argv) > 3):
        vat_percentage = float(sys.argv[3])
    else:
        vat_percentage = 24

    # use local data for testing 
    if (len(sys.argv) > 4) and (sys.argv[4] == 'debug'):
        use_local_data = True
    else:
        use_local_data = False

    if use_local_data:
        root = get_local_data() 
    else:
        data = get_online_data(eic_code)
        root = ET.fromstring(data)

    parser = EntsoEDataParser(root)
    prices = parser.parse_data(root, vat_percentage, utc_diff)
    print_prices(prices)

