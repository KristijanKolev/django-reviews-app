from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Create your tests here.


class UserSignupViewTests(TestCase):
    def test_successful(self):
        response = self.client.post(reverse('user_management:signup'), data={
            'username': 'test_user',
            'password': '1234567',
            'confirm_password': '1234567',
            'email': 'test_user@test.com',
            'bio': 'test_user bio'
        })

        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='test_user')
        self.assertEqual(user.email, 'test_user@test.com')
        self.assertEqual(user.profile.bio, 'test_user bio')
        self.assertTrue(user.check_password('1234567'))

    def test_passwords_mismatch(self):
        response = self.client.post(reverse('user_management:signup'), data={
            'username': 'test_user',
            'password': '1234567',
            'confirm_password': '2234567',
            'email': 'test_user@test.com',
            'bio': 'test_user bio'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords don't match!", html=True)
        # Test that the user does not exist in the DB.
        query_set = User.objects.filter(username='test_user')
        self.assertEqual(query_set.count(), 0)

    def test_name_duplicate(self):
        self.client.post(reverse('user_management:signup'), data={
            'username': 'test_user',
            'password': '1234567',
            'confirm_password': '1234567',
            'email': 'test_user@test.com',
            'bio': 'test_user bio'
        })
        # Call to create a second, identical user
        response = self.client.post(reverse('user_management:signup'), data={
            'username': 'test_user',
            'password': '1234567',
            'confirm_password': '1234567',
            'email': 'duplicate@test.com',
            'bio': 'duplicate bio'
        })
        self.assertContains(response, "Name already taken! Try a different one.", html=True)
        # Test that only the first user was created.
        query_set = User.objects.filter(username='test_user')
        self.assertEqual(query_set.count(), 1)
        self.assertEqual(query_set[0].email, 'test_user@test.com')
        self.assertEqual(query_set[0].profile.bio, 'test_user bio')
