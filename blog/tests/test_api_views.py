from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from blog.models import Article, Event
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from blog.tests.test_utils import create_test_image

class ArticleAPIViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Set the Authorization header with the Bearer token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        
        # Create a valid in-memory image file
        self.image = create_test_image()

        # Create a test article
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article content.",
            image=self.image
        )


    def test_article_list_api_view(self):
        response = self.client.get(reverse('article_list_create_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Article")

    def test_article_detail_api_view(self):
        response = self.client.get(reverse('article_detail_api', args=[self.article.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Article")

    def test_article_create_api_view(self):
        data = {
            "title": "New Test Article",
            "content": "This is another test article content.",
            "image": create_test_image()
        }
        response = self.client.post(reverse('article_list_create_api'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Test Article")

class EventAPIViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Set the Authorization header with the Bearer token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        
        # Create a valid in-memory image file
        self.image = create_test_image()

        # Create a test event
        self.event = Event.objects.create(
            title="Test Event",
            content="This is a test event content.",
            start_date="2024-09-01 10:00:00",
            end_date="2024-09-01 12:00:00",
            image=self.image
        )


    def test_event_list_api_view(self):
        response = self.client.get(reverse('event_list_create_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Event")

    def test_event_detail_api_view(self):
        response = self.client.get(reverse('event_detail_api', args=[self.event.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Event")

    def test_event_create_api_view(self):
        data = {
            "title": "New Test Event",
            "content": "This is another test event content.",
            "start_date": "2024-09-10 10:00:00",
            "end_date": "2024-09-10 12:00:00",
            "image": create_test_image()
        }
        response = self.client.post(reverse('event_list_create_api'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Test Event")
