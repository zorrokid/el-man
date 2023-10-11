import os
import sys
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from models.price import Price

TOKEN = os.environ.get('TOKEN')
API_URL = 'https://web-api.tp.entsoe.eu/api'
EIC_CODE = '10YFI-1--------U'

XML_NAMESPACE = '{urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0}' 

def get_data(url):
    r = requests.get(url)
    if r.status_code != 200:
        error = r.text
        print("Error fetching data from the API", error)
        return None
    return r.text

# Entso-E 4.2.10. Day Ahead Prices [12.1.D]
#    One year range limit applies
#    Minimum time interval in query response is one day
#    Mandatory parameters
#        DocumentType
#        In_Domain
#        Out_Domain
#        TimeInterval or combination of PeriodStart and PeriodEnd
#    In_Domain and Out_Domain must be populated with the same area EIC code
#
# example:
#   GET /api?
#   documentType=A44&
#   in_Domain=10YCZ-CEPS-----N
#   &out_Domain=10YCZ-CEPS-----N
#   &periodStart=201512312300
#   &periodEnd=201612312300


def get_url(date_from: datetime, date_to: datetime, eic_code):
    url = API_URL + '?documentType=A44' + '&in_Domain=' + eic_code + '&out_Domain=' + \
        eic_code + '&periodStart=' + date_to_url(date_from) + \
        '&periodEnd=' + \
        date_to_url(date_to) + '&securityToken=' + TOKEN
    return url

def date_to_url(date: datetime):
    return date.strftime("%Y%m%d%H00")

def with_xml_namespace(tag):
    return XML_NAMESPACE + tag

def get_local_data():
    tree = ET.parse('./example_data/example_result.xml')
    root = tree.getroot()
    return root

def get_online_data(eic_code):
    date_from = datetime.now()
    date_to = date_from + timedelta(days=1)
    url = get_url(date_from, date_to, eic_code)
    data = get_data(url)
    root = ET.fromstring(data)
    return root

def parse_data(root, vat_percentage, utc_diff):
    # find period tags inside timeseries
    key = ".//{0}Period".format(XML_NAMESPACE)
    prices = []
    for period in root.findall(key):
        parse_period_data(period, vat_percentage, utc_diff)
        prices += parse_period_data(period, vat_percentage, utc_diff)
    return prices
    
def parse_period_data(period, vat_percentage, utc_diff):
    interval = period.find(with_xml_namespace("timeInterval"))
    start = interval.find(with_xml_namespace("start"))
    start_time = datetime.fromisoformat(start.text) + timedelta(hours=utc_diff)
    prices = []
    for point in period.iter(with_xml_namespace('Point')):
        parse_point_data(point, start_time, vat_percentage)
        price = parse_point_data(point, start_time, vat_percentage)
        prices.append(price)
    return prices

def parse_point_data(point, start_time, vat_percentage):
    current_time = point_to_time(point, start_time) 
    price_euros_mwh = point_to_price(point) 
    price_cents_kwh = price_to_cents_kwh(price_euros_mwh)
    price_cents_kwh_with_vat = price_with_vat(price_cents_kwh, vat_percentage) 
    price = Price(current_time, price_cents_kwh_with_vat)
    return price 

def point_to_price(point):
    price_element = point.find(with_xml_namespace('price.amount'))
    price_euros_mwh = float(price_element.text)
    return price_euros_mwh

def point_to_time(point, start_time):
    position_element = point.find(with_xml_namespace('position'))
    position = int(position_element.text)
    current_time = start_time + timedelta(hours=position-1) 
    return current_time

def price_to_cents_kwh(price_mwh):
    price_kwh = price_mwh / 1000
    price_cents_kwh = price_kwh * 100
    return price_cents_kwh

def price_with_vat(price, vat_percentage):
    return price * (1 + vat_percentage / 100)

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
        root = get_online_data(eic_code)

    prices = parse_data(root, vat_percentage, utc_diff)
    print_prices(prices)

