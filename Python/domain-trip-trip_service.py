# Trip Management

from datetime import datetime
from typing import Optional

class Trip:
    def __init__(self, trip_id: str, booking_id: str, driver_id: str, 
                 passenger_id: str, vehicle_id: str):
        self.trip_id = trip_id
        self.booking_id = booking_id
        self.driver_id = driver_id
        self.passenger_id = passenger_id
        self.vehicle_id = vehicle_id
        self.start_time = None
        self.end_time = None
        self.pickup_location = None
        self.dropoff_location = None
        self.route = []
        self.fare = None
        self.status = "created"
        self.payment_id = None

    def start(self, pickup_location: dict):
        self.start_time = datetime.utcnow()
        self.pickup_location = pickup_location
        self.status = "in_progress"

    def update_route(self, current_location: dict):
        self.route.append({
            'timestamp': datetime.utcnow(),
            'location': current_location
        })

    def complete(self, dropoff_location: dict, fare: float, payment_id: str):
        self.end_time = datetime.utcnow()
        self.dropoff_location = dropoff_location
        self.fare = fare
        self.payment_id = payment_id
        self.status = "completed"

class TripService:
    def __init__(self):
        self.active_trips = {}
        self.trip_history = {}

    def create_trip(self, booking: Booking) -> Trip:
        trip = Trip(
            trip_id=f"trip_{len(self.trip_history) + 1}",
            booking_id=booking.booking_id,
            driver_id=booking.driver_id,
            passenger_id=booking.passenger_id,
            vehicle_id=booking.vehicle_id
        )
        self.active_trips[trip.trip_id] = trip
        return trip

    def complete_trip(self, trip_id: str, dropoff_location: dict, 
                     fare: float, payment_id: str):
        if trip_id not in self.active_trips:
            raise ValueError("Trip not found")
            
        trip = self.active_trips.pop(trip_id)
        trip.complete(dropoff_location, fare, payment_id)
        self.trip_history[trip_id] = trip
        return trip