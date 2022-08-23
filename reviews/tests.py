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

    def test_nonexistent_search(self):
        self._create_dataset()
        response = self.client.get(f"{reverse('reviews:places_all')}?search=nonexistent_word")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No places found')

    def test_search_and_paging_fetch(self):
        places = self._create_dataset()
        response = self.client.get(f"{reverse('reviews:places_all')}?search=th&page=2&page_size=4")
        self.assertQuerysetEqual(
            response.context['page_obj'],
            [places[5], places[4], places[3], places[2]]
        )


class PlaceDetailsViewTests(TestCase):
    @staticmethod
    def _create_place():
        place = Place.objects.create(name='Test place name', description='Test place description')
        user = get_user_model().objects.create(username='test_user', password='test_password')
        place.review_set.create(comment='Test comment 1', score=5, author=user)
        place.review_set.create(comment='Test comment 2', score=8, author=user)
        place.review_set.create(comment='Test comment 3', score=3, author=user)
        return place

    def _create_and_login_user(self):
        user = get_user_model().objects.create(username='login_user')
        user.set_password('12345')
        user.save()
        self.client.login(username='login_user', password='12345')

    def test_successful(self):
        self._create_and_login_user()
        place = self._create_place()
        response = self.client.get(reverse("reviews:place_details_public", args=(place.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['place'], place)

    def test_nonexistent_id(self):
        self._create_and_login_user()
        self._create_place()
        response = self.client.get(reverse("reviews:place_details_public", args=(1000,)))
        self.assertEqual(response.status_code, 404)

    def test_login_redirect(self):
        place = self._create_place()
        response = self.client.get(reverse("reviews:place_details_public", args=(place.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/user-management/login?next=/places/{place.id}')

    def test_review_creation(self):
        self._create_and_login_user()
        place = self._create_place()
        redirect_response = self.client.post(reverse('reviews:leave_review', args=(place.id,)),
                                             data={'score': 7, 'comment': 'Lorem ipsum'})
        response = self.client.get(redirect_response.url)
        self.assertEqual(response.context['place'].sorted_reviews().count(), 4)
        last_review = response.context['place'].sorted_reviews()[0]
        self.assertEqual(last_review.score, 7)
        self.assertEqual(last_review.comment, 'Lorem ipsum')

    def test_not_logged_in_review_creation(self):
        place = self._create_place()
        response = self.client.post(reverse('reviews:leave_review', args=(place.id,)),
                                             data={'score': 7, 'comment': 'Lorem ipsum'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/user-management/login?next=/places/{place.id}/leave-review')
