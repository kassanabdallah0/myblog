from django.test import TestCase
from blog.forms import SignupForm, ContactForm, ArticleForm, EventForm
from datetime import datetime
from blog.tests.test_utils import create_test_image, delete_test_image

class SignupFormTest(TestCase):

    def test_signup_form_valid(self):
        form = SignupForm(data={
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        form = SignupForm(data={
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
        })
        self.assertFalse(form.is_valid())

class ContactFormTest(TestCase):

    def test_contact_form_valid(self):
        form = ContactForm(data={
            'email': 'test@example.com',
            'request_type': 'contact',
            'message': 'This is a test message.',
        })
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid(self):
        form = ContactForm(data={
            'email': 'test@example.com',
            'request_type': 'contact',
            'message': 'Short.',  # This should now be invalid due to length
        })
        if form.is_valid():
            print("Form should be invalid but is valid. Errors:", form.errors)
        self.assertFalse(form.is_valid())

class ArticleFormTest(TestCase):

    def setUp(self):
        self.image = create_test_image()

    def tearDown(self):
        delete_test_image(self.image.name)

    def test_article_form_valid(self):
        form = ArticleForm(data={
            'title': 'Test Article',
            'content': 'This is a test article content.',
        }, files={
            'image': self.image
        })
        if not form.is_valid():
            print("Form is invalid. Errors:", form.errors)
        self.assertTrue(form.is_valid())

class EventFormTest(TestCase):

    def setUp(self):
        self.image = create_test_image()

    def tearDown(self):
        delete_test_image(self.image.name)

    def test_event_form_valid(self):
        form = EventForm(data={
            'title': 'Test Event',
            'content': 'This is a test event content.',
            'start_date': datetime(2024, 9, 1, 10, 0),
            'end_date': datetime(2024, 9, 1, 12, 0),
        }, files={
            'image': self.image
        })
        if not form.is_valid():
            print("Form is invalid. Errors:", form.errors)
        self.assertTrue(form.is_valid())
