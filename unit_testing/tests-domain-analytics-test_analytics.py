# Test Analytics 

import unittest
from datetime import datetime
from domain.analytics.analytics_service import AnalyticsEngine

class TestAnalyticsEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AnalyticsEngine()
        self.trip_data = {
            "trip_id": "trip123",
            "driver_id": "driver456",
            "city": "bangalore",
            "fare": 250.0,
            "driver_earnings": 200.0,
            "timestamp": datetime.utcnow()
        }

    def test_record_trip(self):
        self.engine.record_trip(self.trip_data)
        self.assertEqual(len(self.engine.trip_data), 1)
        
        # Check city metrics
        self.assertEqual(self.engine.city_metrics["bangalore"]["total_trips"], 1)
        self.assertEqual(self.engine.city_metrics["bangalore"]["total_revenue"], 250.0)
        
        # Check driver metrics
        self.assertEqual(self.engine.driver_metrics["driver456"]["total_trips"], 1)
        self.assertEqual(self.engine.driver_metrics["driver456"]["total_earnings"], 200.0)

    def test_multiple_trips(self):
        # Record multiple trips for same driver and city
        self.engine.record_trip(self.trip_data)
        self.engine.record_trip({
            **self.trip_data,
            "trip_id": "trip124",
            "fare": 300.0,
            "driver_earnings": 240.0
        })
        
        # Check aggregated metrics
        self.assertEqual(self.engine.city_metrics["bangalore"]["total_trips"], 2)
        self.assertEqual(self.engine.city_metrics["bangalore"]["total_revenue"], 550.0)
        self.assertEqual(self.engine.driver_metrics["driver456"]["total_earnings"], 440.0)

    def test_get_metrics(self):
        self.engine.record_trip(self.trip_data)
        
        city_metrics = self.engine.get_city_metrics("bangalore")
        self.assertEqual(city_metrics["total_trips"], 1)
        
        driver_metrics = self.engine.get_driver_metrics("driver456")
        self.assertEqual(driver_metrics["total_trips"], 1)
        
        # Test non-existent entries
        self.assertEqual(self.engine.get_city_metrics("mumbai"), {})
        self.assertEqual(self.engine.get_driver_metrics("driver000"), {})

if __name__ == '__main__':
    unittest.main()