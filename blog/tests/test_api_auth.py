from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework_simplejwt.tokens import RefreshToken
from blog.tests.test_utils import create_test_image

class APIAuthTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Set the Authorization header with the Bearer token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)


    def test_post_article_with_authentication(self):
        # Create the image using the helper function
        image_file = create_test_image()
        
        data = {
            "title": "Authorized Article",
            "content": "This is allowed.",
            "image": image_file
        }
        
        response = self.client.post(reverse('article_list_create_api'), data, format='multipart')
        
        if response.status_code != status.HTTP_201_CREATED:
            print("Response status code:", response.status_code)
            print("Response data:", response.data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
