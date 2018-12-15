from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
import factory


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User


class AuthAPITestCase(APITestCase):
    test_username = 'test_user'
    test_password = 'test_password'

    def setUp(self):
        user = UserFactory(username=self.test_username)
        user.set_password(self.test_password)
        user.save()

    def tearDown(self):
        self.client.credentials()

    def test_login_should_success(self):
        url = reverse('api:login')
        data = {
            "username": self.test_username,
            "password": self.test_password
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json().get('token'))

    def test_login_should_fail(self):
        url = reverse('api:login')
        data = {
            "username": self.test_username,
            "password": self.test_password + '1'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
