import unittest
from domain.target_temperature import calculate_target_temperature

from models.heating_settings import HeatingSettings, get_default_heating_settings

class TestTargetTemperature(unittest.TestCase):

    def test_target_temperature_price_is_none(self):
        price = None
        settings = get_default_heating_settings()
        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(False, heating_enabled) 
        self.assertEqual(0, target_temperature)

    def test_target_temperature_zero_price(self):
        price = 0.0
        settings = HeatingSettings(
            maxPrice=10.0,
            lowPrice=5.0,
            heatingEnabled=True,
            heatingMaxTemperature=20.0,
            heatingMidTemperature=15.0,
            heatingMinTemperature=10.0
        )

        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(heating_enabled, True)
        self.assertEqual(target_temperature, settings.heatingMaxTemperature)

    def test_target_temperature_zero_price_heating_disabled(self):
        price = 0.0
        settings = HeatingSettings(
            maxPrice=10.0,
            lowPrice=5.0,
            heatingEnabled=False,
            heatingMaxTemperature=20.0,
            heatingMidTemperature=15.0,
            heatingMinTemperature=10.0
        )

        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(heating_enabled, False)
        self.assertEqual(target_temperature, 0)

    def test_target_temperature_price_exceed_max(self):
        price = 20.0
        settings = HeatingSettings(
            maxPrice=10.0,
            lowPrice=5.0,
            heatingEnabled=True,
            heatingMaxTemperature=20.0,
            heatingMidTemperature=15.0,
            heatingMinTemperature=10.0
        )

        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(heating_enabled, False)
        self.assertEqual(target_temperature, 0)

    def test_target_temperature_price_below_max(self):
        price = 9.99
        settings = HeatingSettings(
            maxPrice=10.0,
            lowPrice=5.0,
            heatingEnabled=True,
            heatingMaxTemperature=20.0,
            heatingMidTemperature=15.0,
            heatingMinTemperature=10.0
        )

        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(heating_enabled, True)
        self.assertEqual(target_temperature, settings.heatingMidTemperature)

    def test_target_temperature_price_below_low(self):
        price = 4.99
        settings = HeatingSettings(
            maxPrice=10.0,
            lowPrice=5.0,
            heatingEnabled=True,
            heatingMaxTemperature=20.0,
            heatingMidTemperature=15.0,
            heatingMinTemperature=10.0
        )

        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(heating_enabled, True)
        self.assertEqual(target_temperature, settings.heatingMaxTemperature)


if __name__ == '__main__':
    unittest.main()