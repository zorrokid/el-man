"""Test heating settings repository functionality."""
from unittest import TestCase, main
from mockfirestore import MockFirestore
from models.heating_settings import DEFAULT_MAX_PRICE
from repositories.heating_settings import get_heating_settings
from repositories.firestore_collection_constants import HEATING_SETTINGS_COLLECTION

class HeatingSettingsTest(TestCase):
    """Unit tests for the heating settings repository."""
    def test_get_heating_settings(self):
        """Test that heating settings are fetched correctly from Firestore 
        and all the needed fields are populated."""

        # Arrange
        key = '123'
        mock_firestore_client = MockFirestore()
        mock_firestore_client.collection(HEATING_SETTINGS_COLLECTION).document(key).set({
            'maxPrice': 10,
            'lowPrice': 5,
            'heatingEnabled': True,
            'heatingMaxTemperature': 20,
            'heatingMinTemperature': 5,
            'heatingMidTemperature': 10
        })

        # Act
        settings_map = get_heating_settings(mock_firestore_client, {key})

        # Assert
        self.assertTrue(key in settings_map)
        settings = settings_map[key]
        self.assertEqual(settings.heating_enabled, True)
        self.assertEqual(settings.max_price, 10)
        self.assertEqual(settings.low_price, 5)
        self.assertEqual(settings.heating_max_temperature, 20)
        self.assertEqual(settings.heating_min_temperature, 5)
        self.assertEqual(settings.heating_mid_temperature, 10)

    def test_default_settings(self):
        """Test that default settings are used when no settings are found from Firestore."""

        # Arrange
        key = '123'
        mock_firestore_client = MockFirestore()
        
        # Act
        settings_map = get_heating_settings(mock_firestore_client, {key})

        # Assert
        self.assertTrue(key in settings_map)
        settings = settings_map[key]
        self.assertEqual(settings.max_price, DEFAULT_MAX_PRICE)

if __name__ == "__main__":
    main()
