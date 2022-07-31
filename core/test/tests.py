from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Quote

class QuoteTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quote.objects.count(), 1)
        self.assertEqual(Quote.objects.get().name, 'DabApps')
