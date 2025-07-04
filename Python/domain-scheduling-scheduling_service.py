# Driver Scheduling

from datetime import datetime, timedelta

class DriverSchedule:
    def __init__(self, driver_id: str):
        self.driver_id = driver_id
        self.shifts = []
        self.weekly_hours = 0
        self.max_weekly_hours = 48  # India-specific regulation

    def add_shift(self, start_time: datetime, end_time: datetime):
        # Check if shift overlaps with existing shifts
        for shift in self.shifts:
            if not (end_time <= shift['start_time'] or start_time >= shift['end_time']):
                raise ValueError("Shift overlaps with existing shift")
                
        duration = (end_time - start_time).total_seconds() / 3600
        if self.weekly_hours + duration > self.max_weekly_hours:
            raise ValueError("Exceeds maximum weekly working hours")
            
        self.shifts.append({
            'start_time': start_time,
            'end_time': end_time,
            'duration_hours': duration
        })
        self.weekly_hours += duration

class SchedulingService:
    def __init__(self):
        self.schedules = {}

    def get_driver_schedule(self, driver_id: str) -> DriverSchedule:
        if driver_id not in self.schedules:
            self.schedules[driver_id] = DriverSchedule(driver_id)
        return self.schedules[driver_id]

    def assign_shift(self, driver_id: str, start_time: datetime, 
                    end_time: datetime) -> bool:
        schedule = self.get_driver_schedule(driver_id)
        try:
            schedule.add_shift(start_time, end_time)
            return True
        except ValueError as e:
            print(f"Failed to assign shift: {str(e)}")
            return False