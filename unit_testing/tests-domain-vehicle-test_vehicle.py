# Test Vehicle 

import unittest
from datetime import datetime, timedelta
from domain.vehicle.models import Vehicle, VehicleType

class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.vehicle = Vehicle(
            vehicle_id="veh123",
            registration_number="KA01AB1234",
            vehicle_type=VehicleType.SEDAN,
            make="Toyota",
            model="Camry",
            year=2020
        )

    def test_vehicle_initialization(self):
        self.assertEqual(self.vehicle.vehicle_type, VehicleType.SEDAN)
        self.assertTrue(self.vehicle.is_active)
        self.assertIsNone(self.vehicle.current_driver_id)

    def test_driver_assignment(self):
        self.vehicle.assign_driver("driver456")
        self.assertEqual(self.vehicle.current_driver_id, "driver456")

    def test_insurance_update(self):
        details = {"provider": "ICICI", "expiry": "2024-12-31"}
        self.vehicle.update_insurance(details)
        self.assertEqual(self.vehicle.insurance_details, details)

    def test_service_marking(self):
        self.assertFalse(self.vehicle.service_due)
        self.vehicle.mark_service_due()
        self.assertTrue(self.vehicle.service_due)
        self.vehicle.complete_service()
        self.assertFalse(self.vehicle.service_due)
        self.assertIsNotNone(self.vehicle.last_service_date)

if __name__ == '__main__':
    unittest.main()