from unittest.mock import patch

from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ContactSubmission


class ContactSubmissionCreateViewTests(APITestCase):
    def setUp(self):
        self.url = '/api/contact/'
        self.payload = {
            'name': 'Taylor Example',
            'email': 'taylor@example.com',
            'business_name': 'Example Co',
            'project_type': 'Website redesign',
            'budget_range': '$3k - $8k',
            'timeline': '4-6 weeks',
            'message': 'Looking for help improving our site.',
        }

    @override_settings(SMTP2GO_API_KEY='')
    def test_submission_is_saved_even_when_email_delivery_is_unavailable(self):
        response = self.client.post(self.url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactSubmission.objects.count(), 1)
        self.assertFalse(response.data['notification_delivered'])
        self.assertIn('SMTP2GO', response.data['detail'])

    @override_settings(
        SMTP2GO_API_KEY='test-key',
        CONTACT_FORM_TO_EMAIL='hello@cardenstudio.com',
    )
    def test_submission_returns_success_when_email_delivery_succeeds(self):
        with patch('contact.views.ContactSubmissionCreateView.send_notification_email', return_value=None):
            response = self.client.post(self.url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactSubmission.objects.count(), 1)
        self.assertTrue(response.data['notification_delivered'])
        self.assertNotIn('detail', response.data)
