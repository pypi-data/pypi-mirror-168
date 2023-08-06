from django.test import TestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIRequestFactory

from .models import ExampleModel
from .views import ExampleModelViewSet


class VersionedModelViewSetTestCase(TestCase):

    fixtures = ['examples.json']

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_list(self):
        request = self.factory.get('/examples/')
        example_list_view = ExampleModelViewSet.as_view({'get': 'list'})
        response = example_list_view(request)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_retrieve(self):
        request = self.factory.get('/examples/')
        example_detail_view = ExampleModelViewSet.as_view({'get': 'retrieve'})
        response = example_detail_view(request, name='data-analytics-with-python')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], 'data-analytics-with-python')
        self.assertEqual(response.data['version'], '0.1.0')
        self.assertEqual(response.data['updated_at'], "2022-05-23T00:00:00")

    def test_create(self):
        data = {
          "name": "cloud-computing-with-python",
          "created_at": "2022-05-23T00:00:00",
          "version": "0.1.0",
          "title": "Python云计算入门",
          "updated_at": "2022-06-25T00:00:00"
        }
        request = self.factory.post('/courses/', data)
        example_list_view = ExampleModelViewSet.as_view({'post': 'create'})
        response = example_list_view(request, name='cloud-computing-with-python')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'cloud-computing-with-python')
        self.assertEqual(response.data['version'], '0.1.0')
        self.assertEqual(response.data['created_at'], "2022-05-23T00:00:00")
        self.assertEqual(response.data['updated_at'], "2022-06-25T00:00:00")

    def test_update(self):
        data = {
          "name": "data-analytics-with-python",
          "created_at": "2022-05-23T00:00:00",
          "version": "0.2.0",
          "title": "Python数据分析",
          "updated_at": "2022-07-25T00:00:00"
        }
        request = self.factory.put('/courses/', data)
        example_detail_view = ExampleModelViewSet.as_view({'put': 'update'})
        response = example_detail_view(request, name='data-analytics-with-python')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], 'data-analytics-with-python')
        self.assertEqual(response.data['version'], '0.2.0')
        self.assertEqual(response.data['title'], "Python数据分析")
        self.assertEqual(response.data['created_at'], "2022-05-23T00:00:00")
        self.assertEqual(response.data['updated_at'], "2022-07-25T00:00:00")

    def test_partial_update(self):
        data = {
          "name": "data-analytics-with-python",
          "version": "0.2.1",
          "updated_at": "2022-07-26T00:00:00"
        }
        request = self.factory.patch('/courses/', data)
        example_detail_view = ExampleModelViewSet.as_view({'patch': 'partial_update'})
        response = example_detail_view(request, name='data-analytics-with-python')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], 'data-analytics-with-python')
        self.assertEqual(response.data['version'], '0.2.1')
        self.assertEqual(response.data['title'], "Python数据分析")
        self.assertEqual(response.data['created_at'], "2022-05-23T00:00:00")
        self.assertEqual(response.data['updated_at'], "2022-07-26T00:00:00")

    def test_delete(self):
        request = self.factory.delete('/courses/')
        example_detail_view = ExampleModelViewSet.as_view({'delete': 'destroy'})
        response = example_detail_view(request, name='data-analytics-with-python')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertFalse(ExampleModel.objects.get(name='data-analytics-with-python').is_active)

