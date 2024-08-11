from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Article
from blog.tests.test_utils import create_test_image

class WebAuthTest(TestCase):


    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article content.",
            image=create_test_image()
        )

    def test_access_article_list_without_login(self):
        response = self.client.get(reverse('article_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('article_list')}")

    def test_access_article_list_with_login(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Article")

    def test_access_article_create_without_login(self):
        response = self.client.get(reverse('article_create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('article_create')}")

    def test_access_article_create_with_login(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('article_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_article_with_login(self):
        self.client.login(username='testuser', password='testpassword')
        image = create_test_image()
        data = {
            "title": "Authorized Article",
            "content": "This is allowed.",
            "image": image
        }
        response = self.client.post(reverse('article_create'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Authorized Article")  # Check if the new article is in the response
