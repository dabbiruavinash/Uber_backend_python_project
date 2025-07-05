# Test Location 

import unittest
from domain.location.location_service import LocationService

class TestLocationService(unittest.TestCase):
    def setUp(self):
        self.service = LocationService()
        self.bangalore = (12.9716, 77.5946)  # MG Road
        self.whitefield = (12.9698, 77.7499)  # ITPL
        self.drivers = [
            {"current_location": {"latitude": 12.9716, "longitude": 77.5946}, "id": "d1"},
            {"current_location": {"latitude": 12.9698, "longitude": 77.7499}, "id": "d2"},
            {"current_location": {"latitude": 13.0827, "longitude": 80.2707}, "id": "d3"},  # Chennai
            {"current_location": None, "id": "d4"}
        ]

    def test_haversine_distance(self):
        distance = self.service.haversine_distance(*self.bangalore, *self.whitefield)
        self.assertAlmostEqual(distance, 15.7, delta=0.5)  # ~15.7 km between points

    def test_find_nearest_drivers(self):
        pickup = {"latitude": self.bangalore[0], "longitude": self.bangalore[1]}
        nearby = self.service.find_nearest_drivers(self.drivers, pickup, 20.0)
        self.assertEqual(len(nearby), 2)
        self.assertEqual(nearby[0][0]["id"], "d1")  # Closest first
        self.assertLess(nearby[0][1], nearby[1][1])

    def test_no_nearby_drivers(self):
        pickup = {"latitude": 28.6139, "longitude": 77.2090}  # Delhi
        nearby = self.service.find_nearest_drivers(self.drivers, pickup, 5.0)
        self.assertEqual(len(nearby), 0)

if __name__ == '__main__':
    unittest.main()