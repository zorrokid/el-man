"""Contains parser for ENTSO-E XML data"""
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from typing import List
from models.price import Price

XML_NAMESPACE = '{urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0}'

class EntsoEDataParser:
    """Parses ENTSO-E XML data"""
    def __init__(self, data):
        self.data = data

    def with_xml_namespace(self, tag):
        """Returns tag with ENTSO-E XML namespace"""
        return XML_NAMESPACE + tag

    def parse_dayahead_prices(self, vat_percentage, utc_diff) -> List[Price]:
        """Parse day ahead prices from XML data"""
        root = ET.fromstring(self.data)
        # find period tags inside timeseries
        key = f".//{XML_NAMESPACE}Period"
        prices = []
        for period in root.findall(key):
            self.parse_period_data(period, vat_percentage, utc_diff)
            prices += self.parse_period_data(period, vat_percentage, utc_diff)
        return prices

    def parse_period_data(self, period, vat_percentage, utc_diff):
        """Parse period data from XML data"""
        interval = period.find(self.with_xml_namespace("timeInterval"))
        start = interval.find(self.with_xml_namespace("start"))
        start_time = datetime.fromisoformat(start.text) + timedelta(hours=utc_diff)
        prices = []
        for point in period.iter(self.with_xml_namespace('Point')):
            price = self.parse_point_data(point, start_time, vat_percentage)
            prices.append(price)
        return prices

    def parse_point_data(self, point, start_time, vat_percentage):
        """Parse point data from XML data"""
        current_time = self.point_to_time(point, start_time)
        price_euros_mwh = self.point_to_price(point)
        price_cents_kwh = self.price_to_cents_kwh(price_euros_mwh)
        price_cents_kwh_with_vat = self.price_with_vat(price_cents_kwh, vat_percentage)
        price = Price(current_time, price_cents_kwh_with_vat)
        return price 

    def point_to_price(self, point):
        """Parse price from point"""
        price_element = point.find(self.with_xml_namespace('price.amount'))
        price_euros_mwh = float(price_element.text)
        return price_euros_mwh

    def point_to_time(self, point, start_time):
        """Parse time from point"""
        position_element = point.find(self.with_xml_namespace('position'))
        position = int(position_element.text)
        current_time = start_time + timedelta(hours=position-1)
        return current_time

    def price_to_cents_kwh(self, price_mwh):
        """Convert price from €/MWh to cents/kWh"""
        price_euros_kwh = price_mwh / 1000
        price_cents_kwh = price_euros_kwh * 100
        return price_cents_kwh

    def price_with_vat(self, price, vat_percentage):
        """Calculate price with VAT"""
        return price * (1 + vat_percentage / 100)
