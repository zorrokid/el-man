"""Test heating settings repository functionality."""
from unittest import TestCase, main
from mockfirestore import MockFirestore
from repositories.heating_settings import get_heating_settings

class HeatingSettingsTest(TestCase):
    """Unit tests for the heating settings repository."""
    def test_get_heating_settings(self):
        """Test that heating settings are fetched correctly from Firestore."""
        # Arrange
        mock_firestore_client = MockFirestore()
        mock_firestore_client.collection('HeatingSettings').document('123').set({
            'maxPrice': 0,
            'lowPrice': 0,
            'heatingEnabled': True,
            'heatingMaxTemperature': 0,
            'heatingMinTemperature': 0,
            'heatingMidTemperature': 0
        })
        # Act
        settings_map = get_heating_settings(mock_firestore_client, {'123'})

        # Assert
        self.assertTrue('123' in settings_map)
        self.assertEqual(settings_map['123'].heating_enabled, True)


if __name__ == "__main__":
    main()
