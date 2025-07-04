# Location Services

import math
from typing import Optional

class LocationSerivce:
       EARTH_RADIUS_KM = 6371

       @staticmethod
       def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate the great-circle distance between two points"""
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return LocationService.EARTH_RADIUS_KM * c
    
       @staticmethod
       def find_nearest_drivers(drivers: list, pickup_location: dict, radius_km: float = 5.0) -> list:
        """Filter drivers within a certain radius of pickup location"""
        pickup_lat = pickup_location['latitude']
        pickup_lon = pickup_location['longitude']
        
        nearby_drivers = []
        for driver in drivers:
            if not driver.current_location:
                continue
                
            distance = LocationService.haversine_distance(
                pickup_lat, pickup_lon,
                driver.current_location['latitude'],
                driver.current_location['longitude'])
            
            if distance <= radius_km:
                nearby_drivers.append((driver, distance))
        
            # Sort by distance
             return sorted(nearby_drivers, key=lambda x: x[1])