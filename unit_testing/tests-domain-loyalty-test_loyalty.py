# Test Loyalty 

import unittest
from domain.loyalty.loyalty_service import LoyaltyProgram, LoyaltyTier

class TestLoyaltyProgram(unittest.TestCase):
    def setUp(self):
        self.program = LoyaltyProgram()

    def test_initial_tier(self):
        self.assertEqual(self.program.user_points.get("user123"), None)
        
        # Add first points
        self.program.add_points("user123", 5)
        self.assertEqual(self.program.user_points["user123"]["tier"], LoyaltyTier.BLUE)

    def test_tier_upgrades(self):
        # Silver tier
        self.program.add_points("user456", 15)
        self.assertEqual(self.program.user_points["user456"]["tier"], LoyaltyTier.SILVER)
        
        # Gold tier
        self.program.add_points("user456", 40)  # Total 55
        self.assertEqual(self.program.user_points["user456"]["tier"], LoyaltyTier.GOLD)
        
        # Platinum tier
        self.program.add_points("user456", 50)  # Total 105
        self.assertEqual(self.program.user_points["user456"]["tier"], LoyaltyTier.PLATINUM)

    def test_benefits(self):
        self.program.add_points("user789", 10)  # Silver
        benefits = self.program.get_benefits("user789")
        self.assertEqual(benefits["discount"], 5)
        self.assertFalse(benefits["priority_support"])
        
        self.program.add_points("user789", 50)  # Gold
        benefits = self.program.get_benefits("user789")
        self.assertEqual(benefits["discount"], 10)
        self.assertTrue(benefits["priority_support"])

    def test_nonexistent_user(self):
        benefits = self.program.get_benefits("nonexistent")
        self.assertEqual(benefits["discount"], 0)
        self.assertFalse(benefits["priority_support"])

if __name__ == '__main__':
    unittest.main()