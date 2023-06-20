import os
import requests
import datetime

TOKEN = os.environ.get('TOKEN')
API_URL = 'https://web-api.tp.entsoe.eu/api'
EIC_CODE_IN = '10YFI-1--------U'
EIC_CODE_OUT = '10YFI-1--------U'


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


def get_url(date_from: datetime, date_to: datetime, eic_code_in=EIC_CODE_IN, eic_code_out=EIC_CODE_OUT):
    url = API_URL + '?documentType=A44' + '&in_Domain=' + eic_code_in + '&out_Domain=' + \
        eic_code_out + '&periodStart=' + date_to_url(date_from) + \
        '&periodEnd=' + \
        date_to_url(date_to) + '&securityToken=' + TOKEN
    return url


def date_to_url(date: datetime):
    return date.strftime("%Y%m%d%H00")


if __name__ == '__main__':
    if (TOKEN is None):
        print("Please set TOKEN environment variable")
        exit(1)

    date_from = datetime.datetime.now()
    date_to = date_from + datetime.timedelta(days=1)

    url = get_url(date_from, date_to)
    data = get_data(url)
    if data:
        print(data)
