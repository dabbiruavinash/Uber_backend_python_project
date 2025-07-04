# Rating System 

from typing import Optional

class Rating:
    def __init__(self, trip_id: str, rated_entity_id: str, rater_id: str, entity_type: str, score: int, comment: Optional[str] = None):
        if score < 1 or score > 5:
            raise ValueError("Rating score must be between 1 and 5")
            
        self.trip_id = trip_id
        self.rated_entity_id = rated_entity_id
        self.rater_id = rater_id
        self.entity_type = entity_type  # 'driver' or 'passenger'
        self.score = score
        self.comment = comment
        self.created_at = datetime.utcnow()

class RatingService:
    def __init__(self):
        self.ratings = []

    def submit_rating(self, rating: Rating):
        self.ratings.append(rating)

    def get_average_rating(self, entity_id: str, entity_type: str) -> float:
        relevant_ratings = [
            r.score for r in self.ratings 
            if r.rated_entity_id == entity_id and r.entity_type == entity_type]
        
        if not relevant_ratings:
            return 0.0
            
        return sum(relevant_ratings) / len(relevant_ratings)

    def get_ratings_for_entity(self, entity_id: str, entity_type: str) -> list:
        return [
            r for r in self.ratings 
            if r.rated_entity_id == entity_id and r.entity_type == entity_type]