from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Place, Review


class PlaceModelTests(TestCase):
    def test_average_review_score_with_no_reviews(self):
        """
        average_review_score returns None if a Place has no Reviews.
        """
        place = Place.objects.create(name='test')
        self.assertIsNone(place.average_review_score())

    def test_average_review_score_with_reviews(self):
        place = Place.objects.create(name='test', description='')
        user = get_user_model().objects.create(username='test_user', password='test_password')
        place.review_set.create(comment='Test comment 1', score=5, author=user)
        place.review_set.create(comment='Test comment 2', score=8, author=user)
        place.review_set.create(comment='Test comment 3', score=3, author=user)

        self.assertAlmostEqual(place.average_review_score(), 5.33333, places=5)


