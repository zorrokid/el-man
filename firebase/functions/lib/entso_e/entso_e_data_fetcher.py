"""Client to get Entso-E Day Ahead prices"""
from datetime import datetime, timedelta
import requests

API_URL = 'https://web-api.tp.entsoe.eu/api'

TIMEOUT_SECONDS = 10

class EntsoEDataFetcher:
    """Client to get Entso-E Day Ahead prices"""
    def __init__(self, token):
        self.token = token

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

    def get_dayahead_data(self, eic_code) -> str:
        """Get day ahead prices for given EIC code"""
        date_from = datetime.now()
        date_to = date_from + timedelta(days=1)
        url = self.get_url(date_from, date_to, eic_code)
        r = requests.get(url, timeout=TIMEOUT_SECONDS)
        if r.status_code != 200:
            error = r.text
            print("Error fetching data from the API", error)
            return None
        return r.text

    def date_to_url(self, date: datetime) -> str:
        """Convert date to URL format"""
        return date.strftime("%Y%m%d%H00")

    def get_url(self, date_from: datetime, date_to: datetime, eic_code) -> str:
        """Get URL for given date range and EIC code"""
        url = API_URL + '?documentType=A44' + '&in_Domain=' + eic_code + '&out_Domain=' + \
            eic_code + '&periodStart=' + self.date_to_url(date_from) + \
            '&periodEnd=' + \
            self.date_to_url(date_to) + '&securityToken=' + self.token 
        return url
