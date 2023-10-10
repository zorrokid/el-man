import os
import sys
import requests
import datetime
import xml.etree.ElementTree as ET

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

if __name__ == '__main__':
    if (TOKEN is None):
        print("Please set TOKEN environment variable")
        exit(1)

    # read command line argument for Domain EIC Code
    if len(sys.argv) > 1:
       eic_code = sys.argv[1]
    else:
        eic_code = EIC_CODE

    date_from = datetime.datetime.now()
    date_to = date_from + datetime.timedelta(days=1)

    url = get_url(date_from, date_to, eic_code)
    data = get_data(url)
    root = ET.fromstring(data)
    # tree = ET.parse('./example_data/example_result.xml')
    # root = tree.getroot()

    # find period tags inside timeseries
    key = ".//{0}Period".format(XML_NAMESPACE)

    for period in root.findall(key):
        interval = period.find(with_xml_namespace("timeInterval"))
        start = interval.find(with_xml_namespace("start"))
        end = interval.find(with_xml_namespace("end"))
        print("Start: ", start.text)
        print("End: ", end.text)
        for point in period.iter(with_xml_namespace('Point')):
            position = point.find(with_xml_namespace('position'))
            price = point.find(with_xml_namespace('price.amount'))
            print("Position: ", position.text)
            print("Price: ", price.text)
