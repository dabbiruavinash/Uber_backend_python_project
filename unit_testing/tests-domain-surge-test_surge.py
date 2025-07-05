# Test Surge Pricing 

import unittest
from datetime import datetime, time
from domain.surge.surge_pricing import SurgeCalculator

class TestSurgeCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = SurgeCalculator()

    def test_weekday_multiplier(self):
        # Wednesday 2 PM (non-peak)
        test_time = datetime(2023, 6, 14, 14, 0)  # Wednesday
        multiplier = self.calculator.calculate_surge_multiplier(1.0, {})
        self.assertEqual(multiplier, 1.0)

    def test_weekend_multiplier(self):
        # Saturday 11 AM
        test_time = datetime(2023, 6, 17, 11, 0)  # Saturday
        multiplier = self.calculator.calculate_surge_multiplier(1.0, {})
        self.assertEqual(multiplier, 1.2)

    def test_peak_hours_multiplier(self):
        # Weekday 8 AM (peak)
        test_time = datetime(2023, 6, 14, 8, 0)  # Wednesday
        multiplier = self.calculator.calculate_surge_multiplier(1.0, {})
        self.assertEqual(multiplier, 1.5)

    def test_late_night_multiplier(self):
        # Weekday 11 PM (late night)
        test_time = datetime(2023, 6, 14, 23, 0)  # Wednesday
        multiplier = self.calculator.calculate_surge_multiplier(1.0, {})
        self.assertEqual(multiplier, 1.3)

    def test_demand_multiplier(self):
        # High demand
        multiplier = self.calculator.calculate_surge_multiplier(2.0, {})
        self.assertEqual(multiplier, 2.5)

        # Medium demand
        multiplier = self.calculator.calculate_surge_multiplier(1.2, {})
        self.assertEqual(multiplier, 1.8)

    def test_multiplier_cap(self):
        # Very high demand during peak hours
        multiplier = self.calculator.calculate_surge_multiplier(3.0, {})
        self.assertEqual(multiplier, 3.0)  # Capped at 3.0

if __name__ == '__main__':
    unittest.main()