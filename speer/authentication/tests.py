from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User


class AuthenticationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = '/api/auth/signup/'
        self.login_url = '/api/auth/login/'

    def test_signup(self):
        response = self.client.post(self.signup_url, {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Password123!"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login(self):
        # First, create a user
        User.objects.create_user(
            username="testuser", email="testuser@example.com", password="Password123!")
        response = self.client.post(self.login_url, {
            "email": "testuser@example.com",
            "password": "Password123!"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
