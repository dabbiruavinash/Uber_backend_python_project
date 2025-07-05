# Test Scheduling 

import unittest
from datetime import datetime, timedelta
from domain.scheduling.scheduling_service import DriverSchedule, SchedulingService

class TestSchedulingService(unittest.TestCase):
    def setUp(self):
        self.service = SchedulingService()
        self.driver_id = "driver123"
        self.start_time = datetime(2023, 6, 1, 8, 0)
        self.end_time = datetime(2023, 6, 1, 17, 0)

    def test_single_shift(self):
        schedule = DriverSchedule(self.driver_id)
        schedule.add_shift(self.start_time, self.end_time)
        
        self.assertEqual(len(schedule.shifts), 1)
        self.assertEqual(schedule.weekly_hours, 9)

    def test_shift_overlap(self):
        schedule = DriverSchedule(self.driver_id)
        schedule.add_shift(self.start_time, self.end_time)
        
        # Overlapping shift
        with self.assertRaises(ValueError):
            schedule.add_shift(
                datetime(2023, 6, 1, 16, 0),
                datetime(2023, 6, 1, 20, 0)
            )

    def test_max_hours(self):
        schedule = DriverSchedule(self.driver_id)
        
        # Add multiple shifts totaling 48 hours
        for day in range(6):  # Monday to Saturday
            schedule.add_shift(
                datetime(2023, 6, 5 + day, 8, 0),
                datetime(2023, 6, 5 + day, 16, 0)
            )
        
        # Try to add one more shift (should fail)
        with self.assertRaises(ValueError):
            schedule.add_shift(
                datetime(2023, 6, 11, 8, 0),  # Sunday
                datetime(2023, 6, 11, 9, 0)
            )

    def test_service_operations(self):
        # Assign shift through service
        result = self.service.assign_shift(self.driver_id, self.start_time, self.end_time)
        self.assertTrue(result)
        
        # Check schedule
        schedule = self.service.get_driver_schedule(self.driver_id)
        self.assertEqual(len(schedule.shifts), 1)
        
        # Try overlapping shift
        result = self.service.assign_shift(
            self.driver_id,
            datetime(2023, 6, 1, 16, 0),
            datetime(2023, 6, 1, 20, 0)
        )
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()