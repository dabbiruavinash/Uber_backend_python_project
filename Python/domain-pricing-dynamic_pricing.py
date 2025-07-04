# Dynamic Pricing

from datetime import datetime

class PricingStrategy(ABC):
       @abstractmethod
       def calculate_price(self, base_fare: float, distance: float, duration: float, demand_multiplier: float) -> float:
            pass

class StandardPricing(PricingStrategy):
    def calculate_price(self, base_fare: float, distance: float, 
                       duration: float, demand_multiplier: float) -> float:
        return base_fare + (distance * 10) + (duration * 1) * demand_multiplier

class PremiumPricing(PricingStrategy):
    def calculate_price(self, base_fare: float, distance: float, 
                       duration: float, demand_multiplier: float) -> float:
        return (base_fare * 1.5) + (distance * 15) + (duration * 1.5) * demand_multiplier


class PricingEngine:
    def __init__(self):
        self.strategies = {
            'standard': StandardPricing(),
            'premium': PremiumPricing()
        }
        self.base_fares = {
            'mini': 40,
            'sedan': 60,
            'suv': 80,
            'premium': 100
        }

     def get_price_estimate(self, vehicle_type: str, distance: float, 
                          duration: float, demand_multiplier: float = 1.0) -> float:
        if vehicle_type not in self.base_fares:
            raise ValueError("Invalid vehicle type")
            
        strategy = self.strategies['premium' if vehicle_type == 'premium' else 'standard']
        return strategy.calculate_price(
            self.base_fares[vehicle_type],
            distance,
            duration,
            demand_multiplier
        )
