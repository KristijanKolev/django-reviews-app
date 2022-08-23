from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

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


class PlaceListViewTests(TestCase):
    @staticmethod
    def _create_dataset():
        return [
            Place.objects.create(name="Place first", description=""),
            Place.objects.create(name="Place second", description=""),
            Place.objects.create(name="Place third", description=""),
            Place.objects.create(name="Place fourth", description=""),
            Place.objects.create(name="Place fifth", description=""),
            Place.objects.create(name="Place sixth", description=""),
            Place.objects.create(name="Place seventh", description=""),
            Place.objects.create(name="Place eighth", description=""),
            Place.objects.create(name="Place ninth", description=""),
            Place.objects.create(name="Place tenth", description="")
        ]

    def test_no_places(self):
        response = self.client.get(reverse('reviews:places_all'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No places found')

    def test_default_paged_fetch(self):
        places = self._create_dataset()
        response = self.client.get(reverse('reviews:places_all'))
        self.assertQuerysetEqual(response.context['page_obj'], reversed(places[-5:]))

    def test_custom_page_size_fetch(self):
        places = self._create_dataset()
        response = self.client.get(f"{reverse('reviews:places_all')}?page_size=3")
        self.assertQuerysetEqual(response.context['page_obj'], reversed(places[-3:]))

    def test_custom_page_fetch(self):
        places = self._create_dataset()
        response = self.client.get(f"{reverse('reviews:places_all')}?page=2")
        self.assertQuerysetEqual(response.context['page_obj'], reversed(places[:5]))

    def test_nonexistent_page_fetch(self):
        response = self.client.get(f"{reverse('reviews:places_all')}?page=20")
        self.assertEqual(response.status_code, 404)
        
    def test_search_fetch(self):
        places = self._create_dataset()
        response = self.client.get(f"{reverse('reviews:places_all')}?search=se")
        self.assertQuerysetEqual(
            response.context['page_obj'],
            [places[6], places[1]]
        )

    def test_search_and_paging_fetch(self):
        places = self._create_dataset()
        response = self.client.get(f"{reverse('reviews:places_all')}?search=th&page=2&page_size=4")
        self.assertQuerysetEqual(
            response.context['page_obj'],
            [places[5], places[4], places[3], places[2]]
        )

