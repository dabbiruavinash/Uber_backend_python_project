# Test Driver 

import unittest
from domain.driver.models import Driver, DriverStatus

class TestDriver(unittest.TestCase):
     def setUp(self):
            self.driver = Driver(
                  driver_id="driver123",
                  name="Rajesh Kumar",
                  phone="+919876543210",
                  vehicle_id="vehicle456")

    def test_initial_status(self):
        self.assertEqual(self.driver.status, DriverStatus.OFFLINE)

    def test_status_update(self):
        self.driver.update_status(DriverStatus.AVAILABLE)
        self.assertEqual(self.driver.status, DriverStatus.AVAILABLE)

    def test_location_update(self):
        location = {"latitude": 12.9716, "longitude": 77.5946}
        self.driver.update_location(location)
        self.assertEqual(self.driver.current_location, location)

    def test_document_verification(self):
        self.assertFalse(self.driver.is_verified)
        self.driver.add_document("license", "http://example.com/license.jpg")
        self.driver.add_document("rc", "http://example.com/rc.jpg")
        self.driver.add_document("insurance", "http://example.com/insurance.jpg")
        self.driver.verify()
        self.assertTrue(self.driver.is_verified)

if __name__ == '__main__':
    unittest.main()