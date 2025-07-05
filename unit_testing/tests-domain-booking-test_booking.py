# Test Booking 

import unittest
from datetime import datetime
from domain.booking.models import Booking, BookingStatus

class TestBooking(unittest.TestCase):
    def setUp(self):
             self.booking = Booking(
                   booking_id="book123",
                   passenger_id="user456",
                   pickup_location={"latitude": 12.9716, "longitude": 77.5946},
                   dropoff_location={"latitude": 12.9352, "longitude": 77.6245},
                   vehicle_type="sedan")

    def test_initial_status(self):
        self.assertEqual(self.booking.status, BookingStatus.PENDING)

    def test_confirm_booking(self):
        self.booking.confirm("driver789", 250.0)
        self.assertEqual(self.booking.status, BookingStatus.CONFIRMED)
        self.assertEqual(self.booking.driver_id, "driver789")
        self.assertEqual(self.booking.estimated_fare, 250.0)

    def test_cancel_booking(self):
        self.booking.cancel()
        self.assertEqual(self.booking.status, BookingStatus.CANCELLED)

    def test_complete_booking(self):
        self.booking.confirm("driver789", 250.0)
        self.booking.complete(230.0)
        self.assertEqual(self.booking.status, BookingStatus.COMPLETED)
        self.assertEqual(self.booking.actual_fare, 230.0)

    def test_cancel_completed_booking(self):
        self.booking.confirm("driver789", 250.0)
        self.booking.complete(230.0)
        with self.assertRaises(Exception):
            self.booking.cancel()

if __name__ == '__main__':
    unittest.main()