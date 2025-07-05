# Test Rating 

import unittest
from domain.rating.rating_service import Rating, RatingService

class TestRatingService(unittest.TestCase):
    def setUp(self):
        self.service = RatingService()
        self.rating1 = Rating(
            trip_id="trip123",
            rated_entity_id="driver456",
            rater_id="user789",
            entity_type="driver",
            score=5,
            comment="Excellent service"
        )
        self.rating2 = Rating(
            trip_id="trip124",
            rated_entity_id="driver456",
            rater_id="user790",
            entity_type="driver",
            score=4
        )
        self.rating3 = Rating(
            trip_id="trip125",
            rated_entity_id="user789",
            rater_id="driver456",
            entity_type="passenger",
            score=3
        )

    def test_rating_submission(self):
        self.service.submit_rating(self.rating1)
        self.assertEqual(len(self.service.ratings), 1)

    def test_average_rating(self):
        self.service.submit_rating(self.rating1)
        self.service.submit_rating(self.rating2)
        
        avg = self.service.get_average_rating("driver456", "driver")
        self.assertEqual(avg, 4.5)
        
        avg = self.service.get_average_rating("nonexistent", "driver")
        self.assertEqual(avg, 0.0)

    def test_entity_ratings(self):
        self.service.submit_rating(self.rating1)
        self.service.submit_rating(self.rating3)
        
        driver_ratings = self.service.get_ratings_for_entity("driver456", "driver")
        self.assertEqual(len(driver_ratings), 1)
        
        passenger_ratings = self.service.get_ratings_for_entity("user789", "passenger")
        self.assertEqual(len(passenger_ratings), 1)

    def test_invalid_rating_score(self):
        with self.assertRaises(ValueError):
            Rating(
                trip_id="trip126",
                rated_entity_id="driver456",
                rater_id="user791",
                entity_type="driver",
                score=6  # Invalid score
            )

if __name__ == '__main__':
    unittest.main()