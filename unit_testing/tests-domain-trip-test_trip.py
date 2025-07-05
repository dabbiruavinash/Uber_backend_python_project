# Test Trip 

import unittest
from datetime import datetime
from domain.trip.trip_service import Trip, TripService

class TestTripService(unittest.TestCase):
    def setUp(self):
        self.service = TripService()
        self.trip_data = {
            "trip_id": "trip123",
            "booking_id": "book456",
            "driver_id": "driver789",
            "passenger_id": "user123",
            "vehicle_id": "veh456"
        }

    def test_trip_creation(self):
        trip = Trip(**self.trip_data)
        self.assertEqual(trip.status, "created")
        self.assertIsNone(trip.start_time)

    def test_trip_start(self):
        trip = Trip(**self.trip_data)
        pickup = {"latitude": 12.9716, "longitude": 77.5946}
        trip.start(pickup)
        self.assertEqual(trip.status, "in_progress")
        self.assertEqual(trip.pickup_location, pickup)
        self.assertIsNotNone(trip.start_time)

    def test_trip_completion(self):
        trip = Trip(**self.trip_data)
        pickup = {"latitude": 12.9716, "longitude": 77.5946}
        dropoff = {"latitude": 12.9352, "longitude": 77.6245}
        
        trip.start(pickup)
        trip.complete(dropoff, 250.0, "pay123")
        
        self.assertEqual(trip.status, "completed")
        self.assertEqual(trip.dropoff_location, dropoff)
        self.assertEqual(trip.fare, 250.0)
        self.assertIsNotNone(trip.end_time)

    def test_trip_service_management(self):
        trip = self.service.create_trip(Trip(**self.trip_data))
        self.assertIn(trip.trip_id, self.service.active_trips)
        
        dropoff = {"latitude": 12.9352, "longitude": 77.6245}
        completed_trip = self.service.complete_trip(trip.trip_id, dropoff, 250.0, "pay123")
        
        self.assertNotIn(trip.trip_id, self.service.active_trips)
        self.assertIn(trip.trip_id, self.service.trip_history)

if __name__ == '__main__':
    unittest.main()