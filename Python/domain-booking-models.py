# Booking Management 

from datetime import datetime
from enum import Enum

class BookingStatus(Enum):
      PENDING = "pending"
      CONFIRMED = "confirmed"
      CANCELLED = "cancelled"
      COMPLETED = "completed"

class Booking:
       def __init__(self, booking_id: str, passenger_id: str, pickup_location: dict, dropoff_location: dict, vehicle_type: str):
            self.booking_id = booking_id
            self.passenger_id = passenger_id
            self.pickup_location = pickup_location
            self.dropoff_location = dropoff_location
            self.vehicle_type = vehicle_type
            self.status = BookingStatus.PENDING
            self.created_at = datetime.utcnow()
            self.driver_id = None
            self.estimated_fare = None
            self.actual_fare = None

       def confirm(self, driver_id: str, estimated_fare: float):
            self.status = BookingStatus.CONFIRMED

       def complete(self, actual_fare: float):
            self.status = BookingStatus.COMPLETED
            self.actual_fare = actual_fare
