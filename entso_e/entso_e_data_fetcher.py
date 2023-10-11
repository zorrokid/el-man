import requests
from datetime import datetime, timedelta

API_URL = 'https://web-api.tp.entsoe.eu/api'

class EntsoEDataFetcher:
    def __init__(self, token):
        self.token = token 

    def get_dayahead_data(self, eic_code):
        date_from = datetime.now()
        date_to = date_from + timedelta(days=1)
        url = self.get_url(date_from, date_to, eic_code)
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

    def date_to_url(self, date: datetime):
        return date.strftime("%Y%m%d%H00")

    def get_url(self, date_from: datetime, date_to: datetime, eic_code):
        url = API_URL + '?documentType=A44' + '&in_Domain=' + eic_code + '&out_Domain=' + \
            eic_code + '&periodStart=' + self.date_to_url(date_from) + \
            '&periodEnd=' + \
            self.date_to_url(date_to) + '&securityToken=' + self.token 
        return url
