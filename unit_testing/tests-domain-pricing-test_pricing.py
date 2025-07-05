# Test Pricing 

import unittest
from domain.pricing.dynamic_pricing import PricingEngine

class TestPricing(unittest.TestCase):
    def setUp(self):
        self.engine = PricingEngine()

    def test_standard_pricing(self):
        price = self.engine.get_price_estimate("mini", 5.0, 15.0)
        self.assertAlmostEqual(price, 40 + (5 * 10) + (15 * 1))

    def test_premium_pricing(self):
        price = self.engine.get_price_estimate("premium", 5.0, 15.0)
        self.assertAlmostEqual(price, (100 * 1.5) + (5 * 15) + (15 * 1.5))

    def test_invalid_vehicle_type(self):
        with self.assertRaises(ValueError):
            self.engine.get_price_estimate("bicycle", 5.0, 15.0)

    def test_demand_multiplier(self):
        price1 = self.engine.get_price_estimate("mini", 5.0, 15.0, 1.0)
        price2 = self.engine.get_price_estimate("mini", 5.0, 15.0, 1.5)
        self.assertGreater(price2, price1)

if __name__ == '__main__':
    unittest.main()
