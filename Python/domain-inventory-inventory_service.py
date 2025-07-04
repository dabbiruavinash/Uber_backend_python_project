# Fleet Inventory

from typing import Dict, List

class FleetInventory:
    def __init__(self):
        self.vehicles = {}
        self.city_allocations = {}
        self.maintenance_schedule = {}

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles[vehicle.vehicle_id] = vehicle
        if vehicle.vehicle_type.value not in self.city_allocations:
            self.city_allocations[vehicle.vehicle_type.value] = {}

    def allocate_vehicle_to_city(self, vehicle_id: str, city: str):
        if vehicle_id not in self.vehicles:
            raise ValueError("Vehicle not found")
            
        vehicle = self.vehicles[vehicle_id]
        if city not in self.city_allocations[vehicle.vehicle_type.value]:
            self.city_allocations[vehicle.vehicle_type.value][city] = []
            
        self.city_allocations[vehicle.vehicle_type.value][city].append(vehicle_id)

    def get_available_vehicles(self, city: str, vehicle_type: str) -> List[str]:
        return self.city_allocations.get(vehicle_type, {}).get(city, [])

    def schedule_maintenance(self, vehicle_id: str, maintenance_date: str):
        if vehicle_id not in self.vehicles:
            raise ValueError("Vehicle not found")
            
        self.maintenance_schedule[vehicle_id] = maintenance_date
        self.vehicles[vehicle_id].mark_service_due()