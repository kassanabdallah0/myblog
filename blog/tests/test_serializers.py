from django.test import TestCase
from blog.serializers import RegisterSerializer, ArticleSerializer, EventSerializer
from blog.models import Article, Event
from django.utils.timezone import make_aware
from datetime import datetime
from blog.tests.test_utils import create_test_image

class RegisterSerializerTest(TestCase):

    def test_register_serializer_valid(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password2': 'testpassword123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_register_serializer_invalid(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password2': 'wrongpassword'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class ArticleSerializerTest(TestCase):

    def setUp(self):
        self.image = create_test_image()
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article content.",
            image=self.image
        )

    def test_article_serializer(self):
        serializer = ArticleSerializer(instance=self.article)
        self.assertEqual(serializer.data['title'], self.article.title)
        self.assertEqual(serializer.data['content'], self.article.content)
        self.assertTrue(serializer.data['image'].startswith('/media/articles/test_image'))

class EventSerializerTest(TestCase):

    def setUp(self):
        self.image = create_test_image(filename="test_event_image.jpg")
        self.event = Event.objects.create(
            title="Test Event",
            content="This is a test event content.",
            start_date=make_aware(datetime(2024, 9, 1, 10, 0)),
            end_date=make_aware(datetime(2024, 9, 1, 12, 0)),
            image=self.image
        )

    def test_event_serializer(self):
        serializer = EventSerializer(instance=self.event)
        self.assertEqual(serializer.data['title'], self.event.title)
        self.assertEqual(serializer.data['content'], self.event.content)
        self.assertIn('/media/events/test_event_image', serializer.data['image'])

