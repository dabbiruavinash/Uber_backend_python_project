# Test Inventory 

import unittest
from domain.inventory.inventory_service import FleetInventory
from domain.vehicle.models import Vehicle, VehicleType

class TestFleetInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = FleetInventory()
        self.vehicle1 = Vehicle(
            vehicle_id="veh123",
            registration_number="KA01AB1234",
            vehicle_type=VehicleType.SEDAN,
            make="Toyota",
            model="Camry",
            year=2020
        )
        self.vehicle2 = Vehicle(
            vehicle_id="veh456",
            registration_number="KA01CD5678",
            vehicle_type=VehicleType.SUV,
            make="Ford",
            model="Endeavour",
            year=2021
        )

    def test_add_vehicle(self):
        self.inventory.add_vehicle(self.vehicle1)
        self.assertIn(self.vehicle1.vehicle_id, self.inventory.vehicles)
        
        # Check city allocation structure created
        self.assertIn(self.vehicle1.vehicle_type.value, self.inventory.city_allocations)

    def test_vehicle_allocation(self):
        self.inventory.add_vehicle(self.vehicle1)
        self.inventory.add_vehicle(self.vehicle2)
        
        # Allocate to cities
        self.inventory.allocate_vehicle_to_city(self.vehicle1.vehicle_id, "bangalore")
        self.inventory.allocate_vehicle_to_city(self.vehicle2.vehicle_id, "delhi")
        
        # Check allocations
        self.assertIn(
            self.vehicle1.vehicle_id,
            self.inventory.city_allocations[VehicleType.SEDAN.value]["bangalore"]
        )
        self.assertIn(
            self.vehicle2.vehicle_id,
            self.inventory.city_allocations[VehicleType.SUV.value]["delhi"]
        )

    def test_get_available_vehicles(self):
        self.inventory.add_vehicle(self.vehicle1)
        self.inventory.allocate_vehicle_to_city(self.vehicle1.vehicle_id, "bangalore")
        
        available = self.inventory.get_available_vehicles("bangalore", VehicleType.SEDAN.value)
        self.assertEqual(len(available), 1)
        self.assertEqual(available[0], self.vehicle1.vehicle_id)
        
        # Test non-existent city/type
        self.assertEqual(
            len(self.inventory.get_available_vehicles("mumbai", VehicleType.SEDAN.value)),
            0
        )
        self.assertEqual(
            len(self.inventory.get_available_vehicles("bangalore", VehicleType.PREMIUM.value)),
            0
        )

    def test_maintenance_scheduling(self):
        self.inventory.add_vehicle(self.vehicle1)
        self.inventory.schedule_maintenance(self.vehicle1.vehicle_id, "2023-06-15")
        
        self.assertEqual(
            self.inventory.maintenance_schedule[self.vehicle1.vehicle_id],
            "2023-06-15"
        )
        self.assertTrue(self.inventory.vehicles[self.vehicle1.vehicle_id].service_due)

if __name__ == '__main__':
    unittest.main()