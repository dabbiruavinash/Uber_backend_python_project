from enum import Enum

class DriverStatus(Enum):
       OFFLINE = "offline"
       AVAILABLE = "available"
       IN_TRIP = "in_trip"
       ON_BREAK = "on_break"

class Driver:
    def __init__(self, driver_id: str, name: str, phone: str, vehicle_id: str):
        self.driver_id = driver_id
        self.name = name
        self.phone = phone
        self.vehicle_id = vehicle_id
        self.status = DriverStatus.OFFLINE
        self.current_location = None
        self.rating = 0.0
        self.total_trips = 0
        self.is_verified = False
        self.documents = {}

    def update_status(self, status : DriverStatus):
        self.status = status

    def update_location(self, location: dict):
        self.current_location = location

    def add_document(self, doc_type: str, doc_url: str):
        self.documents[doc_type] = doc_url

    def verify(self):
        required_doc = ['license', 'rc', 'insurance']
        if all (doc in self.documents for doc in required_doc):
           self.is_verified = True







