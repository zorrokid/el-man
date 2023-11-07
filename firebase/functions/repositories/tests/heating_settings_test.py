"""Test heating settings repository functionality."""
from unittest import TestCase, main
from mockfirestore import MockFirestore
from models.heating_settings import DEFAULT_MAX_PRICE, get_default_heating_settings
from models.heating_settings import heating_settings_from_dict
from repositories.heating_settings import get_heating_settings, init_heating_settings
from repositories.firestore_collection_constants import HEATING_SETTINGS_COLLECTION
from repositories.firestore_collection_constants import ROOMS_COLLECTION

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

    def test_init_heating_settings_room_with_no_settings(self):
        """Test that heating settings are initialized for rooms that don't have settings."""

        # Arrange
        room_id = '123'
        mock_firestore_client = MockFirestore()
        mock_firestore_client.collection(ROOMS_COLLECTION).document(room_id).set({})
        default_heating_settings = get_default_heating_settings()

        # Act
        init_heating_settings(mock_firestore_client, default_heating_settings)

        # Assert
        settings_raw = mock_firestore_client.collection(
            HEATING_SETTINGS_COLLECTION).document(room_id).get()
        self.assertTrue(settings_raw.exists)
        settings = heating_settings_from_dict(settings_raw.to_dict())
        self.assertEqual(settings.max_price, default_heating_settings.max_price)

    def test_init_heating_settings_room_with_existing_settings(self):
        """Test that heating settings are not overwritten for rooms that have existing settings."""

        # Arrange
        room_id = '123'
        mock_firestore_client = MockFirestore()
        mock_firestore_client.collection(ROOMS_COLLECTION).document(room_id).set({})
        default_heating_settings = get_default_heating_settings()
        expected_max_price = default_heating_settings.max_price + 1
        mock_firestore_client.collection(HEATING_SETTINGS_COLLECTION).document(room_id).set({
            'maxPrice': expected_max_price,
            'lowPrice': 5,
            'heatingEnabled': True,
            'heatingMaxTemperature': 20,
            'heatingMinTemperature': 5,
            'heatingMidTemperature': 10
        })

        # Act
        init_heating_settings(mock_firestore_client, default_heating_settings)

        # Assert
        settings_raw = mock_firestore_client.collection(
            HEATING_SETTINGS_COLLECTION).document(room_id).get()
        self.assertTrue(settings_raw.exists)
        settings = heating_settings_from_dict(settings_raw.to_dict())
        self.assertEqual(settings.max_price, expected_max_price)


if __name__ == "__main__":
    main()
