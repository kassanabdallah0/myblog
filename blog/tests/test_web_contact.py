from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class WebContactTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_contact_form_view_without_login(self):
        self.client.logout()  # Ensure client is not authenticated
        response = self.client.get(reverse('contact'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('contact')}")

    def test_contact_form_view_with_login(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact Us")

    def test_submit_contact_form_valid(self):
        data = {
            "email": "test@example.com",
            "request_type": "contact",
            "message": "This is a test message."
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact_success.html')

    def test_submit_contact_form_invalid(self):
        data = {
            "email": "invalid-email",
            "request_type": "contact",
            "message": "Short."
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
        self.assertContains(response, "Enter a valid email address.")
        self.assertContains(response, "The message must be at least 10 characters long.")
