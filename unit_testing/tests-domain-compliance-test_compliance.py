# Test Compliance

import unittest
from domain.compliance.compliance_service import ComplianceChecker

class TestComplianceChecker(unittest.TestCase):
    def setUp(self):
        self.checker = ComplianceChecker()
        self.driver = {
            "documents": {
                "license": "license123",
                "rc": "rc456",
                "insurance": "ins789",
                "puc": "puc012"
            }
        }
        
        self.trips = [
            {"duration_hours": 2, "start_time": "2023-06-01T08:00:00"},
            {"duration_hours": 3, "start_time": "2023-06-01T11:00:00", "break_after": True},
            {"duration_hours": 4, "start_time": "2023-06-01T15:00:00"}
        ]

    def test_compliant_driver(self):
        result = self.checker.check_driver_compliance(self.driver, self.trips)
        self.assertTrue(result['is_compliant'])
        self.assertEqual(len(result['violations']), 0)

    def test_missing_documents(self):
        incomplete_driver = {"documents": {"license": "license123"}}
        result = self.checker.check_driver_compliance(incomplete_driver, [])
        self.assertFalse(result['is_compliant'])
        self.assertIn("missing_rc", result['violations'])
        self.assertIn("missing_insurance", result['violations'])

    def test_driving_hours_violation(self):
        long_trips = [
            {"duration_hours": 5, "start_time": "2023-06-01T08:00:00"},
            {"duration_hours": 5, "start_time": "2023-06-01T14:00:00"}
        ]
        result = self.checker.check_driver_compliance(self.driver, long_trips)
        self.assertFalse(result['is_compliant'])
        self.assertIn("exceeded_max_driving_hours", result['violations'])

    def test_break_violation(self):
        no_break_trips = [
            {"duration_hours": 4.6, "start_time": "2023-06-01T08:00:00"},
            {"duration_hours": 4.6, "start_time": "2023-06-01T13:00:00"}
        ]
        result = self.checker.check_driver_compliance(self.driver, no_break_trips)
        self.assertFalse(result['is_compliant'])
        self.assertIn("missed_mandatory_break", result['violations'])

if __name__ == '__main__':
    unittest.main()