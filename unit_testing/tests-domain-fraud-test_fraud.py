# Test Fraud Detection 

import unittest
from domain.fraud.fraud_detection import FraudDetector

class TestFraudDetector(unittest.TestCase):
    def setUp(self):
        self.detector = FraudDetector()
        self.normal_activities = [
            {"action": "book", "payment_method": "card1"},
            {"action": "complete", "payment_method": "card1"},
            {"action": "book", "payment_method": "card1"},
        ]
        
        self.suspicious_activities = [
            {"action": "book", "payment_method": "card1"},
            {"action": "cancel"},
            {"action": "book", "payment_method": "card2"},
            {"action": "cancel"},
            {"action": "book", "payment_method": "card3"},
            {"action": "cancel"},
        ]

    def test_normal_behavior(self):
        result = self.detector.detect_suspicious_activity("user123", "passenger", self.normal_activities)
        self.assertFalse(result['is_suspicious'])
        self.assertEqual(result['risk_score'], 0)

    def test_high_cancellation_rate(self):
        result = self.detector.detect_suspicious_activity("user456", "passenger", self.suspicious_activities)
        self.assertTrue(result['is_suspicious'])
        self.assertIn('high_cancellation_rate', result['reasons'])
        self.assertGreaterEqual(result['risk_score'], 30)

    def test_multiple_payment_methods(self):
        activities = [
            {"action": "book", "payment_method": "card1"},
            {"action": "book", "payment_method": "card2"},
            {"action": "book", "payment_method": "card3"},
            {"action": "book", "payment_method": "card4"},
        ]
        result = self.detector.detect_suspicious_activity("user789", "passenger", activities)
        self.assertTrue(result['is_suspicious'])
        self.assertIn('multiple_payment_methods', result['reasons'])
        self.assertGreaterEqual(result['risk_score'], 20)

    def test_risk_level_classification(self):
        result = self.detector.detect_suspicious_activity("user999", "passenger", self.suspicious_activities)
        if result['risk_score'] > 40:
            self.assertEqual(result['risk_level'], 'high')
        elif result['risk_score'] > 20:
            self.assertEqual(result['risk_level'], 'medium')
        else:
            self.assertEqual(result['risk_level'], 'low')

if __name__ == '__main__':
    unittest.main()