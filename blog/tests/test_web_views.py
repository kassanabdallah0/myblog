from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Article, Event
from blog.tests.test_utils import create_test_image, delete_test_image

class ArticleWebViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article content.",
            image=create_test_image()
        )

    def tearDown(self):
        # Delete the actual file stored in the model
        delete_test_image(self.article.image.path)

    def test_article_list_view(self):
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Article")

    def test_article_detail_view(self):
        response = self.client.get(reverse('article_detail', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    def test_article_create_view(self):
        new_image = create_test_image()
        data = {
            "title": "New Test Article",
            "content": "This is another test article content.",
            "image": new_image
        }
        try:
            response = self.client.post(reverse('article_create'), data, format='multipart')
            self.assertEqual(response.status_code, 302)  # Redirect after successful creation
            self.assertRedirects(response, reverse('article_list'))
        finally:
            delete_test_image(self.article.image.path)  # Clean up the test image file


class EventWebViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.event = Event.objects.create(
            title="Test Event",
            content="This is a test event content.",
            start_date="2024-09-01 10:00:00",
            end_date="2024-09-01 12:00:00",
            image=create_test_image()
        )

    def tearDown(self):
        # Delete the actual file stored in the model
        delete_test_image(self.event.image.path)

    def test_event_list_view(self):
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")

    def test_event_detail_view(self):
        response = self.client.get(reverse('event_detail', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)

    def test_event_create_view(self):
        new_image = create_test_image()
        data = {
            "title": "New Test Event",
            "content": "This is another test event content.",
            "start_date": "2024-09-10 10:00:00",
            "end_date": "2024-09-10 12:00:00",
            "image": new_image
        }
        try:
            response = self.client.post(reverse('event_create'), data, format='multipart')
            self.assertEqual(response.status_code, 302)  # Redirect after successful creation
            self.assertRedirects(response, reverse('event_list'))
        finally:
            delete_test_image(self.event.image.path)  # Clean up the test image file
