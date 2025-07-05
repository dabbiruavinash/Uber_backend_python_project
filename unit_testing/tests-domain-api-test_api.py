# Test API 

import unittest
from fastapi.testclient import TestClient
from domain.api.gateway import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())

    def test_create_booking(self):
        booking_data = {
            "passenger_id": "user123",
            "pickup_location": {"latitude": 12.9716, "longitude": 77.5946},
            "dropoff_location": {"latitude": 12.9352, "longitude": 77.6245},
            "vehicle_type": "sedan"
        }
        response = self.client.post("/book", json=booking_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("booking_id", response.json())

    def test_invalid_booking(self):
        booking_data = {
            "passenger_id": "user123",
            "pickup_location": None,
            "dropoff_location": {"latitude": 12.9352, "longitude": 77.6245},
            "vehicle_type": "sedan"
        }
        response = self.client.post("/book", json=booking_data)
        self.assertEqual(response.status_code, 400)

    def test_get_nearby_drivers(self):
        response = self.client.get("/drivers/nearby", params={
            "latitude": 12.9716,
            "longitude": 77.5946
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()["drivers"], list)

if __name__ == '__main__':
    unittest.main()