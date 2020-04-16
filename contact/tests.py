from django.test import TestCase, TransactionTestCase
from django.test.utils import override_settings
from unittest.mock import MagicMock, patch
from django.urls import reverse
from django.http import HttpResponseBadRequest
from celery.contrib.testing.worker import start_worker
from portfolio.celery import app
from .forms import ContactForm
from .tasks import mail_admins_async


class ContactViewTestCase(TestCase):
    def test_bio_view(self):
        response = self.client.get(reverse('bio'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)


class ContactFormTestCase(TestCase):
    def test_form_invalid(self):
        form_data = {
            'name': 'Test',
            'email': '',
            'message': 'A message'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_phone_regex(self):
        form_data = {
            'name': 'Test',
            'email': 'test@test.com',
            'phone': '102910a',
            'message': 'A message'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_valid(self):
        form_data = {
            'name': 'Test',
            'email': 'test@test.com',
            'phone': '+10291030293',
            'message': 'A message'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())


class JsonMixinTestCase(TestCase):
    @override_settings(
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
        CELERY_ALWAYS_EAGER=True,
        BROKER_BACKEND='memory'
    )
    @patch('contact.tasks.mail_admins_async.delay', new=MagicMock())
    def test_json_form_submission(self):
        form_data = {
            'name': 'Test',
            'email': 'test@test.com',
            'phone': '+10291030293',
            'message': 'A message',
            'phonenumber': ''
        }
        response = self.client.post(
            reverse('contact'),
            data=form_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.json(), {
            'url': '/',
            'success': True
        })

    def test_honey_pot(self):
        form_data = {
            'name': 'Test',
            'email': 'test@test.com',
            'phone': '+10291030293',
            'message': 'A message',
            'phonenumber': '03290342'
        }
        response = self.client.post(
            reverse('contact'),
            data=form_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertIsInstance(response, HttpResponseBadRequest)
