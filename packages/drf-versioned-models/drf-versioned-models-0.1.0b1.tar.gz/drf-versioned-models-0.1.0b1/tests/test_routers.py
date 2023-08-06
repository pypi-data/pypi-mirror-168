from django.test import TestCase
from django.urls import include, path, reverse, resolve

from rest_framework.test import URLPatternsTestCase
from rest_framework.status import HTTP_200_OK


class VersionedModelRouterTestCase(TestCase, URLPatternsTestCase):
    fixtures = ['examples.json']

    urlpatterns = [
        path('', include('tests.urls'))
    ]

    def test_reverse_example_model_list_url(self):
        url = reverse('tests:examplemodel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_resolve_example_model_list_url(self):
        match = resolve('/examples/')
        self.assertEqual(match.view_name, 'tests:examplemodel-list')

    def test_reverse_example_model_detail_url(self):
        url = reverse('tests:examplemodel-detail', kwargs={'name': 'data-analytics-with-python'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_resolve_example_model_detail_url(self):
        match = resolve('/examples/data-analytics-with-python/')
        self.assertEqual(match.view_name, 'tests:examplemodel-detail')
