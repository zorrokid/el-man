"""Prices test module."""
from datetime import datetime, timedelta
from unittest import TestCase, main
from mockfirestore import MockFirestore
from models.price import Price
from repositories.firestore_collection_constants import PRICES_COLLECTION
from repositories.prices import get_price_for_next_hour_of 


class PricesTest(TestCase):
    """Unit tests for the prices repository."""
    def test_get_price_for_next_hour_of(self):
        """Test that prices are fetched correctly from Firestore 
        and all the needed fields are populated."""

        # Arrange
        now = datetime(2023, 1, 1, 12, 30, 0) # 2023-01-01 12:30:00
        next_hour = now + timedelta(hours=1)
        key_for_next_hour = Price.create_price_key(next_hour)
        mock_firestore_client = MockFirestore()
        mock_firestore_client.collection(PRICES_COLLECTION).document(key_for_next_hour).set({
            'price': 10.0,
            'time': key_for_next_hour
        })

        # Act
        price = get_price_for_next_hour_of(mock_firestore_client, now)

        # Assert
        self.assertEqual(price, 10.0)

    def test_no_price_for_next_hour(self):
        """Test that None is returned when no price is found for next hour."""

        # Arrange
        now = datetime(2023, 1, 1, 12, 30, 0) # 2023-01-01 12:30:00
        mock_firestore_client = MockFirestore()

        # Act
        price = get_price_for_next_hour_of(mock_firestore_client, now)

        # Assert
        self.assertEqual(price, None)

if __name__ == "__main__":
    main()
