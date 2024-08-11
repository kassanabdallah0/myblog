from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class APIContactTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Set the Authorization header with the Bearer token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_contact_api_without_authentication(self):
        self.client.logout()  # Ensure client is not authenticated
        data = {
            "email": "test@example.com",
            "request_type": "contact",
            "message": "This is a test message."
        }
        response = self.client.post(reverse('contact_api'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_contact_api_with_authentication(self):
        data = {
            "email": "test@example.com",
            "request_type": "contact",
            "message": "This is a test message."
        }
        response = self.client.post(reverse('contact_api'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Contact request submitted successfully.")

    def test_contact_api_invalid_data(self):
        data = {
            "email": "invalid-email",
            "request_type": "contact",
            "message": "Short."
        }
        response = self.client.post(reverse('contact_api'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('message', response.data)
