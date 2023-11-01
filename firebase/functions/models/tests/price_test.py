"""Unit tests for price.py."""
from datetime import datetime
import unittest

from models.price import Price

class PriceTest(unittest.TestCase):
    """Unit tests for the price class."""
    def test_get_price_key(self):
        """Test that price key is created correctly."""
        # Arrange
        price = Price(time=datetime(2022, 1, 1, 12, 0, 0), price=100.0)

        # Act
        result = price.get_price_key()

        # Assert
        self.assertEqual(result, "202201011200")

if __name__ == "__main__":
    unittest.main()
