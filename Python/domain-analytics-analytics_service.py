# Analytics Service

from datetime import datetime, timedelta

class AnalyticsEngine:
    def __init__(self):
        self.trip_data = []
        self.booking_data = []
        self.driver_metrics = {}
        self.city_metrics = {}

    def record_trip(self, trip_data: dict):
        self.trip_data.append(trip_data)
        self._update_city_metrics(trip_data)
        self._update_driver_metrics(trip_data)

    def _update_city_metrics(self, trip_data: dict):
        city = trip_data.get('city', 'unknown')
        if city not in self.city_metrics:
            self.city_metrics[city] = {
                'total_trips': 0,
                'total_revenue': 0,
                'last_updated': None
            }
        
        self.city_metrics[city]['total_trips'] += 1
        self.city_metrics[city]['total_revenue'] += trip_data.get('fare', 0)
        self.city_metrics[city]['last_updated'] = datetime.utcnow()

    def _update_driver_metrics(self, trip_data: dict):
        driver_id = trip_data.get('driver_id')
        if not driver_id:
            return
            
        if driver_id not in self.driver_metrics:
            self.driver_metrics[driver_id] = {
                'total_trips': 0,
                'total_earnings': 0,
                'average_rating': 0,
                'last_trip': None
            }
        
        self.driver_metrics[driver_id]['total_trips'] += 1
        self.driver_metrics[driver_id]['total_earnings'] += trip_data.get('driver_earnings', 0)
        self.driver_metrics[driver_id]['last_trip'] = datetime.utcnow()

    def get_city_metrics(self, city: str, time_period: str = "all") -> dict:
        if city not in self.city_metrics:
            return {}
            
        # Filter by time period if needed
        return self.city_metrics[city]

    def get_driver_metrics(self, driver_id: str) -> dict:
        return self.driver_metrics.get(driver_id, {})