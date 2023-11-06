"""Unit tests for the target temperature calculation"""
import unittest
from domain.target_temperature import calculate_target_temperature

from models.heating_settings import HeatingSettings, get_default_heating_settings

class TestTargetTemperature(unittest.TestCase):
    """Unit tests for the target temperature calculation"""

    def test_target_temperature_price_is_none(self):
        """Test that target temperature is zero and heating is disabled when price is None"""
        price = None
        settings = get_default_heating_settings()
        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(False, heating_enabled) 
        self.assertEqual(0, target_temperature)

    def test_target_temperature_zero_price(self):
        """Test that target temperature is max temperature and heating is enabled when price is zero"""
        price = 0.0
        settings = HeatingSettings(
            max_price=10.0,
            low_price=5.0,
            heating_enabled=True,
            heating_max_temperature=20.0,
            heating_mid_temperature=15.0,
            heating_min_temperature=10.0
        )

        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(heating_enabled, True)
        self.assertEqual(target_temperature, settings.heating_max_temperature)

    def test_target_temperature_zero_price_heating_disabled(self):
        """Test that target temperature is zero and heating is 
        disabled when price is zero and heating is disabled"""
        price = 0.0
        settings = HeatingSettings(
            max_price=10.0,
            low_price=5.0,
            heating_enabled=False,
            heating_max_temperature=20.0,
            heating_mid_temperature=15.0,
            heating_min_temperature=10.0
        )

        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(heating_enabled, False)
        self.assertEqual(target_temperature, 0)

    def test_target_temperature_price_exceed_max(self):
        """Test that target temperature is zero and heating 
        is disabled when price exceeds max price"""
        price = 20.0
        settings = HeatingSettings(
            max_price=10.0,
            low_price=5.0,
            heating_enabled=True,
            heating_max_temperature=20.0,
            heating_mid_temperature=15.0,
            heating_min_temperature=10.0
        )

        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(heating_enabled, False)
        self.assertEqual(target_temperature, 0)

    def test_target_temperature_price_below_max(self):
        """Test that target temperature is mid temperature and 
        heating is enabled when price is below max price"""
        price = 9.99
        settings = HeatingSettings(
            max_price=10.0,
            low_price=5.0,
            heating_enabled=True,
            heating_max_temperature=20.0,
            heating_mid_temperature=15.0,
            heating_min_temperature=10.0
        )

        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(heating_enabled, True)
        self.assertEqual(target_temperature, settings.heating_mid_temperature)

    def test_target_temperature_price_below_low(self):
        """Test that target temperature is max temperature and 
        heating is enabled when price is below low price"""
        price = 4.99
        settings = HeatingSettings(
            max_price=10.0,
            low_price=5.0,
            heating_enabled=True,
            heating_max_temperature=20.0,
            heating_mid_temperature=15.0,
            heating_min_temperature=10.0
        )

        (heating_enabled, target_temperature) = calculate_target_temperature(price, settings)
        self.assertEqual(heating_enabled, True)
        self.assertEqual(target_temperature, settings.heating_max_temperature)


if __name__ == '__main__':
    unittest.main()