# Surge Pricing

from datetime import datetime, time

class SurgeCalculator:
    def __init__(self):
        self.base_multipliers = {
            'weekday': 1.0,
            'weekend': 1.2,
            'peak_hours': 1.5,
            'late_night': 1.3
        }
        self.demand_thresholds = {
            'low': 0.7,
            'medium': 1.0,
            'high': 1.5,
            'very_high': 2.0
        }

    def calculate_surge_multiplier(self, demand_factor: float, 
                                  location: dict) -> float:
        """Calculate surge multiplier based on demand and time factors"""
        now = datetime.utcnow()
        is_weekend = now.weekday() >= 5  # Saturday or Sunday
        is_peak_hours = (
            time(7, 0) <= now.time() <= time(10, 0) or 
            time(17, 0) <= now.time() <= time(20, 0)
        )
        is_late_night = time(22, 0) <= now.time() or now.time() <= time(5, 0)

        # Base multiplier based on time
        time_multiplier = 1.0
        if is_weekend:
            time_multiplier = self.base_multipliers['weekend']
        elif is_peak_hours:
            time_multiplier = self.base_multipliers['peak_hours']
        elif is_late_night:
            time_multiplier = self.base_multipliers['late_night']

        # Demand-based multiplier
        demand_multiplier = 1.0
        if demand_factor >= self.demand_thresholds['very_high']:
            demand_multiplier = 2.5
        elif demand_factor >= self.demand_thresholds['high']:
            demand_multiplier = 1.8
        elif demand_factor >= self.demand_thresholds['medium']:
            demand_multiplier = 1.3

        # Combine multipliers with a cap at 3.0
        return min(time_multiplier * demand_multiplier, 3.0)