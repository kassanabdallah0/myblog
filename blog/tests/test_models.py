from django.test import TestCase
from blog.models import Article, Event
from datetime import datetime
from django.utils.timezone import make_aware
from blog.tests.test_utils import create_test_image, delete_test_image

class ArticleModelTest(TestCase):

    def setUp(self):
        self.image = create_test_image(filename="test_article_image.jpg")
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article content.",
            image=self.image
        )

    def tearDown(self):
        delete_test_image(self.article.image.path)

    def test_article_creation(self):
        self.assertIsInstance(self.article, Article)
        self.assertEqual(self.article.title, "Test Article")
        self.assertEqual(self.article.content, "This is a test article content.")
        self.assertTrue(self.article.published_date)
        self.assertTrue(self.article.image)  # Ensure the image is properly associated
        self.assertIn("articles/test_article_image", self.article.image.name)  # Check that the image path includes the expected prefix


class EventModelTest(TestCase):

    def setUp(self):
        self.image = create_test_image(filename="test_event_image.jpg")
        self.event = Event.objects.create(
            title="Test Event",
            content="This is a test event content.",
            start_date=make_aware(datetime(2024, 9, 1, 10, 0)),
            end_date=make_aware(datetime(2024, 9, 1, 12, 0)),
            image=self.image
        )

    def tearDown(self):
        delete_test_image(self.event.image.path)

    def test_event_creation(self):
        self.assertIsInstance(self.event, Event)
        self.assertEqual(self.event.title, "Test Event")
        self.assertEqual(self.event.content, "This is a test event content.")
        self.assertTrue(self.event.published_date)
        self.assertEqual(self.event.start_date, make_aware(datetime(2024, 9, 1, 10, 0)))
        self.assertEqual(self.event.end_date, make_aware(datetime(2024, 9, 1, 12, 0)))
        self.assertTrue(self.event.image)  # Ensure the image is properly associated
        self.assertIn("events/test_event_image", self.event.image.name)
