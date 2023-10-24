import unittest
from models.device import from_dict

class DeviceTest(unittest.TestCase):

    def test_device_from_dict(self):
        dict = {
            'id': 1,
            'name': 'name',
            'energyTime': 1,
            'energyWh': 1,
            'type': 'type'
        }

        device = from_dict(dict)
        self.assertEqual(device.id, 1)
        self.assertEqual(device.name, 'name')
        self.assertEqual(device.energyTime, 1)
        self.assertEqual(device.energyWh, 1)
        self.assertEqual(device.type, 'type')

if __name__ == '__main__':
    unittest.main()