# Loyalty Program


from datetime import datetime

class LoyaltyTier(Enum):
    BLUE = "blue"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"

class LoyaltyProgram:
    TIER_THRESHOLDS = {
        LoyaltyTier.BLUE: 0,
        LoyaltyTier.SILVER: 10,
        LoyaltyTier.GOLD: 50,
        LoyaltyTier.PLATINUM: 100
    }
    
    TIER_BENEFITS = {
        LoyaltyTier.BLUE: {"discount": 0, "priority_support": False},
        LoyaltyTier.SILVER: {"discount": 5, "priority_support": False},
        LoyaltyTier.GOLD: {"discount": 10, "priority_support": True},
        LoyaltyTier.PLATINUM: {"discount": 15, "priority_support": True}
    }

    def __init__(self):
        self.user_points = {}

    def add_points(self, user_id: str, points: int):
        if user_id not in self.user_points:
            self.user_points[user_id] = {
                'total_points': 0,
                'current_points': 0,
                'tier': LoyaltyTier.BLUE
            }
        
        self.user_points[user_id]['current_points'] += points
        self.user_points[user_id]['total_points'] += points
        self._update_tier(user_id)

    def _update_tier(self, user_id: str):
        points = self.user_points[user_id]['total_points']
        new_tier = LoyaltyTier.BLUE
        
        for tier, threshold in sorted(self.TIER_THRESHOLDS.items(), 
                                    key=lambda x: x[1], reverse=True):
            if points >= threshold:
                new_tier = tier
                break
                
        self.user_points[user_id]['tier'] = new_tier

    def get_benefits(self, user_id: str) -> dict:
        if user_id not in self.user_points:
            return self.TIER_BENEFITS[LoyaltyTier.BLUE]
            
        return self.TIER_BENEFITS[self.user_points[user_id]['tier']]