# Vehicle Management

from enum import Enum

class VehicleType(Enum):
        MINI = "mini"
        SEDAN = "sedan"
        SUV = "suv"
        PREMIUM = "premium"
        AUTO = "auto"
        BIKE = "bike"

class Vehicle:
    def __init__(self, vehicle_id: str, registration_number: str, vehicle_type: VehicleType, make: str, model: str, year: int):
        self.vehicle_id = vehicle_id
        self.registration_number = registration_number
        self.vehicle_type = vehicle_type
        self.make = make
        self.model = model
        self.year = year
        self.is_active = True
        self.current_driver_id = None
        self.insurance_details = None
        self.last_service_date = None
        self.service_due = False

    def assign_driver(self, driver_id: str):
        self.current_driver_id = driver_id

    def update_insurance(self, details: dict):
        self.insurance_details = details

    def mark_service_due(self):
        self.service_due = True

    def complete_service(self):
        self.service_due = False
        self.last_service_date = datetime.utcnow().date()